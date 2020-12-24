import json
from collections import deque

import numpy as np
import os
import pickle

from multiprocessing import Pool
from tqdm import tqdm

from data_processing.data_preprocessing_constants import JSON_COUNTS_BY_YEAR, \
    RAW_GAME_LOGS_PATH, EXTRACTED_GAME_LOGS_PATH, SELECTED_YEARS, \
    GAME_LOGS_COUNT, TENHOU_TILE_INDEX, ROUND_NUMBER_SIZE, HONBA_NUMBER_SIZE, \
    DEPOSIT_NUMBER_SIZE, TURN_NUMBER_SIZE, SCORES_SIZE, ONE_SCORE_SIZE, \
    DORA_INDICATORS_SIZE, SELF_RED_DORA_SIZE, MELDS_SIZE, ONE_MELD_SIZE, \
    TILES_SIZE, RIICHI_PLAYERS_SIZE, TOTAL_COLUMNS_SIZE, TOTAL_FEATURES_COUNT, \
    GAME_LOGS_COUNTS_BY_YEAR, DATASET_PATH

from data_processing.player import Player

from hand_calculation.tile_constants import FIVE_MAN, FIVE_PIN, FIVE_SOU, \
    NORTH, RED_FIVE_MAN, RED_FIVE_PIN, RED_FIVE_SOU

SEATING_INDEX = {  # use discard-player-index - pon-player-index
    -1: 0,  # left-hand-side player
    -2: 1,  # opposite player
    2: 1,  # opposite player
    1: 2,  # right-hand-side player
}


def extract_game_logs_from_json(year):
    with tqdm(desc='Extracting ' + year + ' game logs',
              total=JSON_COUNTS_BY_YEAR[year]) as pbar:
        with open(os.path.join(RAW_GAME_LOGS_PATH, year), 'rb') as fread:
            with open(os.path.join(EXTRACTED_GAME_LOGS_PATH, year + '.pickle'),
                      'wb') as fwrite:
                for line in fread:
                    js = json.loads(line)
                    for log in js['log']:
                        pickle.dump(log, fwrite)
                    pbar.update(1)


def count_extracted_game_logs(year):
    count = 0
    with open(os.path.join(EXTRACTED_GAME_LOGS_PATH, year + '.pickle'), 'rb') \
            as fread:
        try:
            while pickle.load(fread):
                count += 1
        except EOFError:
            pass
    return count


def find_max_honba_and_deposit():
    max_honba = 0
    max_honba_year = ''
    max_deposit = 0
    max_deposit_year = ''
    with tqdm(desc='Processing', total=GAME_LOGS_COUNT) as pbar:
        for year in SELECTED_YEARS:
            with open(os.path.join(EXTRACTED_GAME_LOGS_PATH, year + '.pickle'),
                      'rb') as fread:
                try:
                    while log := pickle.load(fread):
                        if log[0][1] > max_honba:
                            max_honba = log[0][1]
                            max_honba_year = year
                        if log[0][2] > max_deposit:
                            max_deposit = log[0][2]
                            max_deposit_year = year
                        pbar.update(1)
                except EOFError:
                    pass
    return {
        'max_honba': max_honba,
        'max_honba_year': max_honba_year,
        'max_deposit': max_deposit,
        'max_deposit_year': max_deposit_year
    }


def encode_tile(tenhou_encoded_tile):
    """
    :param tenhou_encoded_tile: Tenhou-encoded integer index of a tile
    :return: (34, 1) np.array
    """
    output = np.zeros((34, 1))

    tile = TENHOU_TILE_INDEX[tenhou_encoded_tile]
    if tile == RED_FIVE_MAN:
        tile = FIVE_MAN
    elif tile == RED_FIVE_PIN:
        tile = FIVE_PIN
    elif tile == RED_FIVE_SOU:
        tile = FIVE_SOU

    output[tile, :] = 1
    return output


def encode_number(number, size):
    """
    :param round_number: Integer
    :return: (34, size) np.array
    """
    output = np.empty((34, size))
    for bit, val in enumerate(bin(number)[2:].zfill(size)):
        if val == '1':
            output[:, bit] = 1
        else:
            output[:, bit] = 0
    return output


def encode_round_number(round_number):
    """
    :param round_number: log[0][0] from Tenhou
    :return: (34, 3) np.array
    """
    return encode_number(round_number, ROUND_NUMBER_SIZE)


def encode_honba_number(honba_number):
    """
    :param honba_number: log[0][1] from Tenhou
    :return: (34, 4) np.array
    """
    return encode_number(honba_number, HONBA_NUMBER_SIZE)


def encode_deposit_number(deposit_number):
    """
    :param deposit_number: log[0][2] from Tenhou
    :return: (34, 4) np.array
    """
    return encode_number(deposit_number, DEPOSIT_NUMBER_SIZE)


def encode_scores(scores):
    """
    :param scores: log[1] from Tenhou, a list of all 4 player's scores
    :return: (34, 44) np.array
    """
    output = np.zeros((34, SCORES_SIZE))
    for index, score in enumerate(scores):
        for bit, val in enumerate(bin(score // 100)[2:].zfill(ONE_SCORE_SIZE)):
            if val == '1':
                output[:, index * ONE_SCORE_SIZE + bit] = 1
    return output


def encode_dora_indicator(array, dora_indicators, index):
    """
    :param array: (34, 4) np.array, original encoded dora indicators
    :param dora_indicators: log[2] from Tenhou, the list of dora indicators
    :param index: index of the dora indicator from Tenhou's log
    :return: updated (34, 4) np.array
    """
    if TENHOU_TILE_INDEX[dora_indicators[0]] == RED_FIVE_MAN:
        array[FIVE_MAN, index] = 1
    elif TENHOU_TILE_INDEX[dora_indicators[0]] == RED_FIVE_PIN:
        array[FIVE_PIN, index] = 1
    elif TENHOU_TILE_INDEX[dora_indicators[0]] == RED_FIVE_SOU:
        array[FIVE_SOU, index] = 1
    else:
        array[TENHOU_TILE_INDEX[dora_indicators[0]], index] = 1


def connect_bit(x, y):
    return (x << 1) | y


connect_bit = np.frompyfunc(connect_bit, 2, 1)


def to_binary(array):
    array_reshaped = array.reshape(TOTAL_FEATURES_COUNT).astype(int)
    return connect_bit.reduce(array_reshaped)


def to_array(binary):
    return np.array([int(item) for item in
                     list(bin(binary)[2:].zfill(TOTAL_FEATURES_COUNT))]) \
        .reshape((34, TOTAL_COLUMNS_SIZE)).astype(float)


def encode_game_log(log, f_discard, f_pon, f_kan, f_kita, f_riichi,
                    ignore_last_discard=False):
    round_number = encode_round_number(log[0][0])
    honba_number = encode_honba_number(log[0][1])
    deposit_number = encode_deposit_number(log[0][2])
    scores = encode_scores(log[1])
    dora_indicators = np.zeros((34, DORA_INDICATORS_SIZE))
    encode_dora_indicator(dora_indicators, log[2], 0)

    players = [Player(), Player(), Player()]
    hand_index = 4
    for player in players:
        player.encode_start_hand(log[hand_index])
        player.log_draws = deque(log[hand_index + 1])
        player.log_discards = deque(log[hand_index + 2])
        hand_index += 3

    remaining_discards = len(log[6]) + len(log[9]) + len(log[12])
    east_index = log[0][0] % 4
    self_index = east_index
    turn_number = 0
    is_pon = False

    while remaining_discards > 0:
        # Tenhou game log representations:
        # Pon: 'p', in draw
        # Open Kan: 'm', in draw
        # Closed Kan: 'a', in discard
        # Add Kan: 'k', in discard
        # Kita: 'f', in discard
        # Riichi: 'r', in discard
        if self_index == east_index:
            turn_number += 1

        # if turn_number == 9 and self_index == 1:  # TODO: for debugging
        #     assert True  # TODO: for debugging

        player_self = players[self_index]
        player1 = players[(self_index + 1) % 3]
        player2 = players[(self_index + 2) % 3]
        player3 = Player()
        self_wind = encode_tile(self_index % 4 + 41)

        endgame_flag = False

        if not is_pon:
            draw_flag = True
            drawn_tile = player_self.log_draws.popleft()
            action = player_self.log_discards.popleft()
            if action == 60:
                action = drawn_tile
            remaining_discards -= 1

            while draw_flag:
                draw_flag = False
                if player_self.can_kita(drawn_tile):
                    # add state to the the Kita dataset
                    pickle.dump(
                        to_binary(np.concatenate((
                            encode_tile(drawn_tile),
                            player_self.hand,
                            player_self.red_dora,
                            player_self.melds,
                            player_self.kita,
                            player_self.discards,
                            dora_indicators,
                            player1.encode_riichi_status(),
                            player2.encode_riichi_status(),
                            player3.encode_riichi_status(),
                            scores,
                            round_number,
                            honba_number,
                            deposit_number,
                            self_wind,
                            player1.melds,
                            player1.kita,
                            player1.discards,
                            player2.melds,
                            player2.kita,
                            player2.discards,
                            player3.melds,
                            player3.kita,
                            player3.discards
                        ), axis=1)), f_kita)

                    if 'f' in str(action):
                        # add action to the Kita dataset
                        pickle.dump(1, f_kita)

                        # Update state
                        player_self.add_tile_to_hand(drawn_tile)
                        player_self.add_kita()
                        if player_self.log_draws:
                            draw_flag = True
                            drawn_tile = player_self.log_draws.popleft()
                            if remaining_discards > 0:
                                action = player_self.log_discards.popleft()
                                if action == 60:
                                    action = drawn_tile
                                remaining_discards -= 1
                                continue
                            else:
                                endgame_flag = True
                                break
                        else:
                            endgame_flag = True
                            break
                    else:
                        # add action to the Kita dataset
                        pickle.dump(0, f_kita)

                if player_self.can_closed_kan(drawn_tile):
                    # add state to the Kan dataset
                    pickle.dump(
                        to_binary(np.concatenate((
                            encode_tile(drawn_tile),
                            player_self.hand,
                            player_self.red_dora,
                            player_self.melds,
                            player_self.kita,
                            player_self.discards,
                            dora_indicators,
                            player1.encode_riichi_status(),
                            player2.encode_riichi_status(),
                            player3.encode_riichi_status(),
                            scores,
                            round_number,
                            honba_number,
                            deposit_number,
                            self_wind,
                            player1.melds,
                            player1.kita,
                            player1.discards,
                            player2.melds,
                            player2.kita,
                            player2.discards,
                            player3.melds,
                            player3.kita,
                            player3.discards
                        ), axis=1)), f_kan)

                    if 'a' in str(action):
                        # add action to the Kan dataset
                        pickle.dump(1, f_kan)

                        # Update state
                        player_self.add_tile_to_hand(drawn_tile)
                        kan_tile = int(str(action).replace('a', '')[:2])
                        player_self.add_meld('kan', kan_tile, turn_number)

                        kan_tile_converted = TENHOU_TILE_INDEX[kan_tile]
                        if kan_tile_converted == RED_FIVE_MAN:
                            kan_tile_converted = FIVE_MAN
                        elif kan_tile_converted == RED_FIVE_PIN:
                            kan_tile_converted = FIVE_PIN
                        elif kan_tile_converted == RED_FIVE_SOU:
                            kan_tile_converted = FIVE_SOU
                        player_self.meld_tiles.remove(kan_tile_converted)
                        player_self.closed_kan.append(kan_tile_converted)

                        if player_self.log_draws:
                            draw_flag = True
                            drawn_tile = player_self.log_draws.popleft()
                            if remaining_discards > 0:
                                action = player_self.log_discards.popleft()
                                if action == 60:
                                    action = drawn_tile
                                remaining_discards -= 1
                                continue
                            else:
                                endgame_flag = True
                                break
                        else:
                            endgame_flag = True
                            break
                    else:
                        # add action to the Kita dataset
                        pickle.dump(0, f_kan)

                if player_self.can_add_kan(drawn_tile):
                    # add state to the Kan dataset
                    pickle.dump(
                        to_binary(np.concatenate((
                            encode_tile(drawn_tile),
                            player_self.hand,
                            player_self.red_dora,
                            player_self.melds,
                            player_self.kita,
                            player_self.discards,
                            dora_indicators,
                            player1.encode_riichi_status(),
                            player2.encode_riichi_status(),
                            player3.encode_riichi_status(),
                            scores,
                            round_number,
                            honba_number,
                            deposit_number,
                            self_wind,
                            player1.melds,
                            player1.kita,
                            player1.discards,
                            player2.melds,
                            player2.kita,
                            player2.discards,
                            player3.melds,
                            player3.kita,
                            player3.discards
                        ), axis=1)), f_kan)

                    if 'k' in str(action):
                        # add action to the Kan dataset
                        pickle.dump(1, f_kan)

                        # Update state
                        player_self.add_tile_to_hand(drawn_tile)
                        kan_tile = int(str(action).replace('k', '')[:2])
                        player_self.add_meld('kan', kan_tile, turn_number)

                        if player_self.log_draws:
                            draw_flag = True
                            drawn_tile = player_self.log_draws.popleft()
                            if remaining_discards > 0:
                                action = player_self.log_discards.popleft()
                                if action == 60:
                                    action = drawn_tile
                                remaining_discards -= 1
                                continue
                            else:
                                endgame_flag = True
                                break
                        else:
                            endgame_flag = True
                            break
                    else:
                        # add action to the Kita dataset
                        pickle.dump(0, f_kan)

            if endgame_flag:
                break

            if player_self.can_riichi(drawn_tile):
                # add state to the Riichi dataset
                pickle.dump(
                    to_binary(np.concatenate((
                        encode_tile(drawn_tile),
                        player_self.hand,
                        player_self.red_dora,
                        player_self.melds,
                        player_self.kita,
                        player_self.discards,
                        dora_indicators,
                        player1.encode_riichi_status(),
                        player2.encode_riichi_status(),
                        player3.encode_riichi_status(),
                        scores,
                        round_number,
                        honba_number,
                        deposit_number,
                        self_wind,
                        player1.melds,
                        player1.kita,
                        player1.discards,
                        player2.melds,
                        player2.kita,
                        player2.discards,
                        player3.melds,
                        player3.kita,
                        player3.discards
                    ), axis=1)), f_riichi)

                if 'r' in str(action):
                    # add action to the Riichi dataset
                    pickle.dump(1, f_riichi)

                    # add state to the discard dataset
                    pickle.dump(
                        to_binary(np.concatenate((
                            encode_tile(drawn_tile),
                            player_self.hand,
                            player_self.red_dora,
                            player_self.melds,
                            player_self.kita,
                            player_self.discards,
                            dora_indicators,
                            player1.encode_riichi_status(),
                            player2.encode_riichi_status(),
                            player3.encode_riichi_status(),
                            scores,
                            round_number,
                            honba_number,
                            deposit_number,
                            self_wind,
                            player1.melds,
                            player1.kita,
                            player1.discards,
                            player2.melds,
                            player2.kita,
                            player2.discards,
                            player3.melds,
                            player3.kita,
                            player3.discards
                        ), axis=1)), f_discard)

                    # add action to the discard dataset
                    discarded_tile = int(action.replace('r', ''))
                    if discarded_tile == 60:
                        discarded_tile = drawn_tile
                    discarded_tile_converted = TENHOU_TILE_INDEX[discarded_tile]
                    if discarded_tile_converted == RED_FIVE_MAN:
                        discarded_tile_converted = FIVE_MAN
                    elif discarded_tile_converted == RED_FIVE_PIN:
                        discarded_tile_converted = FIVE_PIN
                    elif discarded_tile_converted == RED_FIVE_SOU:
                        discarded_tile_converted = FIVE_SOU
                    pickle.dump(discarded_tile_converted, f_discard)

                    # update state
                    player_self.add_tile_to_hand(drawn_tile)
                    player_self.discard_tile_from_hand(discarded_tile)
                    player_self.riichi_status = True
                    player_self.riichi_turn_number = turn_number

                else:
                    # add action to the Riichi dataset
                    pickle.dump(0, f_riichi)

                    # add state to the discard dataset
                    pickle.dump(
                        to_binary(np.concatenate((
                            encode_tile(drawn_tile),
                            player_self.hand,
                            player_self.red_dora,
                            player_self.melds,
                            player_self.kita,
                            player_self.discards,
                            dora_indicators,
                            player1.encode_riichi_status(),
                            player2.encode_riichi_status(),
                            player3.encode_riichi_status(),
                            scores,
                            round_number,
                            honba_number,
                            deposit_number,
                            self_wind,
                            player1.melds,
                            player1.kita,
                            player1.discards,
                            player2.melds,
                            player2.kita,
                            player2.discards,
                            player3.melds,
                            player3.kita,
                            player3.discards
                        ), axis=1)), f_discard)

                    # add action to the discard dataset
                    discarded_tile = action
                    discarded_tile_converted = TENHOU_TILE_INDEX[discarded_tile]
                    if discarded_tile_converted == RED_FIVE_MAN:
                        discarded_tile_converted = FIVE_MAN
                    elif discarded_tile_converted == RED_FIVE_PIN:
                        discarded_tile_converted = FIVE_PIN
                    elif discarded_tile_converted == RED_FIVE_SOU:
                        discarded_tile_converted = FIVE_SOU
                    pickle.dump(discarded_tile_converted, f_discard)

                    # update state
                    player_self.add_tile_to_hand(drawn_tile)
                    player_self.discard_tile_from_hand(discarded_tile)

            else:
                discarded_tile = action

                # if player hasn't declared Riichi, add data to the
                # discard dataset
                if not player_self.riichi_status:
                    pickle.dump(
                        to_binary(np.concatenate((
                            encode_tile(drawn_tile),
                            player_self.hand,
                            player_self.red_dora,
                            player_self.melds,
                            player_self.kita,
                            player_self.discards,
                            dora_indicators,
                            player1.encode_riichi_status(),
                            player2.encode_riichi_status(),
                            player3.encode_riichi_status(),
                            scores,
                            round_number,
                            honba_number,
                            deposit_number,
                            self_wind,
                            player1.melds,
                            player1.kita,
                            player1.discards,
                            player2.melds,
                            player2.kita,
                            player2.discards,
                            player3.melds,
                            player3.kita,
                            player3.discards
                        ), axis=1)), f_discard)

                    discarded_tile_converted = TENHOU_TILE_INDEX[discarded_tile]
                    if discarded_tile_converted == RED_FIVE_MAN:
                        discarded_tile_converted = FIVE_MAN
                    elif discarded_tile_converted == RED_FIVE_PIN:
                        discarded_tile_converted = FIVE_PIN
                    elif discarded_tile_converted == RED_FIVE_SOU:
                        discarded_tile_converted = FIVE_SOU
                    pickle.dump(discarded_tile_converted, f_discard)

                # update state
                player_self.add_tile_to_hand(drawn_tile)
                player_self.discard_tile_from_hand(discarded_tile)

        else:
            action = player_self.log_discards.popleft()
            if action == 60:
                action = drawn_tile
            discarded_tile = action
            remaining_discards -= 1

            # if player hasn't declared Riichi, add data to the discard dataset
            if not player_self.riichi_status:
                pickle.dump(
                    to_binary(np.concatenate((
                        encode_tile(drawn_tile),
                        player_self.hand,
                        player_self.red_dora,
                        player_self.melds,
                        player_self.kita,
                        player_self.discards,
                        dora_indicators,
                        player1.encode_riichi_status(),
                        player2.encode_riichi_status(),
                        player3.encode_riichi_status(),
                        scores,
                        round_number,
                        honba_number,
                        deposit_number,
                        self_wind,
                        player1.melds,
                        player1.kita,
                        player1.discards,
                        player2.melds,
                        player2.kita,
                        player2.discards,
                        player3.melds,
                        player3.kita,
                        player3.discards
                    ), axis=1)), f_discard)

                discarded_tile_converted = TENHOU_TILE_INDEX[discarded_tile]
                if discarded_tile_converted == RED_FIVE_MAN:
                    discarded_tile_converted = FIVE_MAN
                elif discarded_tile_converted == RED_FIVE_PIN:
                    discarded_tile_converted = FIVE_PIN
                elif discarded_tile_converted == RED_FIVE_SOU:
                    discarded_tile_converted = FIVE_SOU
                pickle.dump(discarded_tile_converted, f_discard)

            # update state
            player_self.add_tile_to_hand(drawn_tile)
            player_self.discard_tile_from_hand(discarded_tile)

        interrupted = False

        for i in range(3):
            if i != self_index \
                    and (not players[i].riichi_status) \
                    and players[i].log_draws:
                action = players[i].log_draws[0]
                if players[i].can_pon(discarded_tile):
                    # add state to the Pon dataset
                    pickle.dump(
                        to_binary(np.concatenate((
                            encode_tile(drawn_tile),
                            players[i].hand,
                            players[i].red_dora,
                            players[i].melds,
                            players[i].kita,
                            players[i].discards,
                            dora_indicators,
                            players[(i + 1) % 3].encode_riichi_status(),
                            players[(i + 2) % 3].encode_riichi_status(),
                            player3.encode_riichi_status(),
                            scores,
                            round_number,
                            honba_number,
                            deposit_number,
                            self_wind,
                            players[(i + 1) % 3].melds,
                            players[(i + 1) % 3].kita,
                            players[(i + 1) % 3].discards,
                            players[(i + 2) % 3].melds,
                            players[(i + 2) % 3].kita,
                            players[(i + 2) % 3].discards,
                            player3.melds,
                            player3.kita,
                            player3.discards
                        ), axis=1)), f_pon)

                    if 'p' in str(action):
                        pon_player = str(action).index('p') / 2
                        seating_diff = self_index - i
                        pon_tile = int(str(action).replace('p', '')[:2])
                        if (pon_tile == discarded_tile
                            or (pon_tile == 15 and discarded_tile == 51)
                            or (pon_tile == 25 and discarded_tile == 52)
                            or (pon_tile == 35 and discarded_tile == 53)
                            or (pon_tile == 51 and discarded_tile == 15)
                            or (pon_tile == 52 and discarded_tile == 25)
                            or (pon_tile == 53 and discarded_tile == 35)) \
                                and SEATING_INDEX[seating_diff] == pon_player:
                            # add action to the Pon dataset
                            pickle.dump(1, f_pon)

                            # update state
                            drawn_tile = discarded_tile
                            players[i].log_draws.popleft()
                            players[i].add_tile_to_hand(drawn_tile)
                            players[i].add_meld('pon', drawn_tile, turn_number)
                            self_index = i
                            is_pon = True
                            interrupted = True
                            break
                        else:
                            # add action to the Pon dataset
                            pickle.dump(0, f_pon)
                            is_pon = False
                            interrupted = False
                    else:
                        # add action to the Pon dataset
                        pickle.dump(0, f_pon)
                        is_pon = False
                        interrupted = False

                if players[i].can_open_kan(discarded_tile):
                    # add state to the Kan dataset
                    pickle.dump(
                        to_binary(np.concatenate((
                            encode_tile(drawn_tile),
                            players[i].hand,
                            players[i].red_dora,
                            players[i].melds,
                            players[i].kita,
                            players[i].discards,
                            dora_indicators,
                            players[(i + 1) % 3].encode_riichi_status(),
                            players[(i + 2) % 3].encode_riichi_status(),
                            player3.encode_riichi_status(),
                            scores,
                            round_number,
                            honba_number,
                            deposit_number,
                            self_wind,
                            players[(i + 1) % 3].melds,
                            players[(i + 1) % 3].kita,
                            players[(i + 1) % 3].discards,
                            players[(i + 2) % 3].melds,
                            players[(i + 2) % 3].kita,
                            players[(i + 2) % 3].discards,
                            player3.melds,
                            player3.kita,
                            player3.discards
                        ), axis=1)), f_kan)

                    if 'm' in str(action):
                        kan_tile = int(str(action).replace('m', '')[:2])
                        if kan_tile == discarded_tile \
                                or (kan_tile == 15 and discarded_tile == 51) \
                                or (kan_tile == 25 and discarded_tile == 52) \
                                or (kan_tile == 35 and discarded_tile == 53) \
                                or (kan_tile == 51 and discarded_tile == 15) \
                                or (kan_tile == 52 and discarded_tile == 25) \
                                or (kan_tile == 53 and discarded_tile == 35):
                            # add action to the Kan dataset
                            pickle.dump(1, f_kan)

                            # update state
                            drawn_tile = discarded_tile
                            players[i].log_draws.popleft()
                            players[i].add_tile_to_hand(drawn_tile)
                            players[i].add_meld('kan', drawn_tile, turn_number)
                            if players[i].log_discards:
                                players[i].log_discards.popleft()
                                remaining_discards -= 1
                            self_index = i
                            is_pon = False
                            interrupted = True
                            break
                        else:
                            # add action to the Kan dataset
                            pickle.dump(0, f_kan)
                            is_pon = False
                            interrupted = False
                    else:
                        # add action to the Kan dataset
                        pickle.dump(0, f_kan)
                        is_pon = False
                        interrupted = False

        if not interrupted:
            self_index = (self_index + 1) % 3
            is_pon = False


if __name__ == '__main__':
    # assert False  # comment this line to confirm running the scripts
    #
    # # Extract game logs from the downloaded JSON objects
    # pool = Pool(len(SELECTED_YEARS))
    # for year in SELECTED_YEARS:
    #     pool.apply_async(extract_game_logs_from_json, args=(year,))
    # pool.close()
    # pool.join()
    #
    # # Count the number of extracted game logs
    # total = 0
    # for year in SELECTED_YEARS:
    #     count = count_extracted_game_logs(year)
    #     print(str(count) + ' game logs extracted from ' + year)
    #     total += count
    # print('Total no. of game logs extracted: ' + str(total))
    #
    # # Find the maximum honba and deposit numbers
    # max_honba_and_deposit_results = find_max_honba_and_deposit()
    # for key, val in max_honba_and_deposit_results.items():
    #     print(key + ':', val)

    with tqdm(desc='Encoding', total=GAME_LOGS_COUNTS_BY_YEAR['2019']) as pbar:
        with open(os.path.join(DATASET_PATH, 'discard' + '.pickle'),
                  'wb') as f_discard:
            with open(os.path.join(DATASET_PATH, 'pon' + '.pickle'),
                      'wb') as f_pon:
                with open(os.path.join(DATASET_PATH, 'kan' + '.pickle'),
                          'wb') as f_kan:
                    with open(os.path.join(DATASET_PATH, 'kita' + '.pickle'),
                              'wb') as f_kita:
                        with open(os.path.join(DATASET_PATH,
                                               'riichi' + '.pickle'),
                                  'wb') as f_riichi:
                            with open(os.path.join(EXTRACTED_GAME_LOGS_PATH,
                                                   '2019' + '.pickle'),
                                      'rb') as fread:
                                try:
                                    # count = 0  # TODO: for debugging

                                    while log := pickle.load(fread):
                                        # count += 1  # TODO: for debugging
                                        # if count != 5743:  # TODO: for debugging
                                        #     continue  # TODO: for debugging

                                        encode_game_log(log,
                                                        f_discard=f_discard,
                                                        f_pon=f_pon,
                                                        f_kan=f_kan,
                                                        f_kita=f_kita,
                                                        f_riichi=f_riichi)
                                        pbar.update(1)
                                except EOFError:
                                    pass
    print('Success')
