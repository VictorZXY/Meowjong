import csv
import json
import os
import pickle
import traceback

import numpy as np

from collections import deque
from PIL import Image
from tqdm import tqdm

from data_processing.data_processing_constants import JSON_COUNTS_BY_YEAR, \
    RAW_GAME_LOGS_PATH, EXTRACTED_GAME_LOGS_PATH, SELECTED_YEARS, \
    GAME_LOGS_COUNT, TENHOU_TILE_INDEX, ROUND_NUMBER_SIZE, HONBA_NUMBER_SIZE, \
    DEPOSIT_NUMBER_SIZE, SCORES_SIZE, ONE_SCORE_SIZE, \
    DORA_INDICATORS_SIZE, TOTAL_COLUMNS_SIZE, TOTAL_FEATURES_COUNT, \
    DATASET_PATH, GAME_LOGS_COUNTS_BY_YEAR, DISCARD_COUNTS, PON_COUNTS, \
    KAN_COUNTS, KITA_COUNTS, RIICHI_COUNTS
from data_processing.player import Player
from evaluation.hand_calculation.tile_constants import FIVE_MAN, FIVE_PIN, \
    FIVE_SOU, RED_FIVE_MAN, RED_FIVE_PIN, RED_FIVE_SOU

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
    :param number: Integer
    :param size: size of the desired np.array
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
    if index >= len(dora_indicators):
        return

    if TENHOU_TILE_INDEX[dora_indicators[index]] == RED_FIVE_MAN:
        array[FIVE_MAN, index] = 1
    elif TENHOU_TILE_INDEX[dora_indicators[index]] == RED_FIVE_PIN:
        array[FIVE_PIN, index] = 1
    elif TENHOU_TILE_INDEX[dora_indicators[index]] == RED_FIVE_SOU:
        array[FIVE_SOU, index] = 1
    else:
        array[TENHOU_TILE_INDEX[dora_indicators[index]], index] = 1


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


def encode_game_log(year, log, dataset_dir, discard_dir, pon_dir, kan_dir,
                    kita_dir, riichi_dir, discard_count, pon_count, kan_count,
                    kita_count, riichi_count):
    """
    :param year: String
    :param log: Tenhou JSON game log object
    :param dataset_dir: Dataset directory
    :param discard_dir: Discard directory
    :param pon_dir: Pon directory
    :param kan_dir: Kan directory
    :param kita_dir: Kita directory
    :param riichi_dir: Riichi directory
    :param discard_count: Integer
    :param pon_count: Dictionary
    :param kan_count: Dictionary
    :param kita_count: Dictionary
    :param riichi_count: Dictionary
    :return: discard_count
    """
    round_number = encode_round_number(log[0][0])
    honba_number = encode_honba_number(log[0][1])
    deposit_number = encode_deposit_number(log[0][2])
    scores = encode_scores(log[1])
    dora_indicators = np.zeros((34, DORA_INDICATORS_SIZE))
    dora_indicator_index = 0
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
                    kita_count['total'] += 1
                    state = np.concatenate((
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
                    ), axis=1).astype(np.uint8)
                    filename = 'kita_' + year + '_' \
                               + str(kita_count['total']) + '.png'
                    Image.fromarray(state * 255, 'L') \
                        .save(os.path.join(kita_dir, filename))

                    if 'f' in str(action):
                        # add action to the Kita dataset
                        filename = 'kita_actions_' + year + '.txt'
                        with open(os.path.join(dataset_dir, filename), 'a') \
                                as f_kita:
                            f_kita.write('1\n')
                        kita_count['yes'] += 1

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
                        filename = 'kita_actions_' + year + '.txt'
                        with open(os.path.join(dataset_dir, filename), 'a') \
                                as f_kita:
                            f_kita.write('0\n')
                        kita_count['no'] += 1

                if player_self.can_closed_kan(drawn_tile):
                    # add state to the Kan dataset
                    kan_count['total'] += 1
                    state = np.concatenate((
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
                    ), axis=1).astype(np.uint8)
                    filename = 'kan_' + year + '_' \
                               + str(kan_count['total']) + '.png'
                    Image.fromarray(state * 255, 'L') \
                        .save(os.path.join(kan_dir, filename))

                    if 'a' in str(action):
                        # add action to the Kan dataset
                        filename = 'kan_actions_' + year + '.txt'
                        with open(os.path.join(dataset_dir, filename), 'a') \
                                as f_kan:
                            f_kan.write('1\n')
                        kan_count['yes'] += 1

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
                            dora_indicator_index += 1
                            encode_dora_indicator(dora_indicators, log[2],
                                                  dora_indicator_index)
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
                        # add action to the Kan dataset
                        filename = 'kan_actions_' + year + '.txt'
                        with open(os.path.join(dataset_dir, filename), 'a') \
                                as f_kan:
                            f_kan.write('0\n')
                        kan_count['no'] += 1

                if player_self.can_add_kan(drawn_tile):
                    # add state to the Kan dataset
                    kan_count['total'] += 1
                    state = np.concatenate((
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
                    ), axis=1).astype(np.uint8)
                    filename = 'kan_' + year + '_' \
                               + str(kan_count['total']) + '.png'
                    Image.fromarray(state * 255, 'L') \
                        .save(os.path.join(kan_dir, filename))

                    if 'k' in str(action):
                        # add action to the Kan dataset
                        filename = 'kan_actions_' + year + '.txt'
                        with open(os.path.join(dataset_dir, filename), 'a') \
                                as f_kan:
                            f_kan.write('1\n')
                        kan_count['yes'] += 1

                        # Update state
                        player_self.add_tile_to_hand(drawn_tile)
                        kan_tile = int(str(action).replace('k', '')[:2])
                        player_self.add_meld('kan', kan_tile, turn_number)

                        if player_self.log_draws:
                            draw_flag = True
                            drawn_tile = player_self.log_draws.popleft()
                            dora_indicator_index += 1
                            encode_dora_indicator(dora_indicators, log[2],
                                                  dora_indicator_index)
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
                        # add action to the Kan dataset
                        filename = 'kan_actions_' + year + '.txt'
                        with open(os.path.join(dataset_dir, filename), 'a') \
                                as f_kan:
                            f_kan.write('0\n')
                        kan_count['no'] += 1

            if endgame_flag:
                break

            if player_self.can_riichi(drawn_tile):
                # add state to the Riichi dataset
                riichi_count['total'] += 1
                state = np.concatenate((
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
                ), axis=1).astype(np.uint8)
                filename = 'riichi_' + year + '_' \
                           + str(riichi_count['total']) + '.png'
                Image.fromarray(state * 255, 'L') \
                    .save(os.path.join(riichi_dir, filename))

                if 'r' in str(action):
                    # add action to the Riichi dataset
                    filename = 'riichi_actions_' + year + '.txt'
                    with open(os.path.join(dataset_dir, filename), 'a') \
                            as f_riichi:
                        f_riichi.write('1\n')
                    riichi_count['yes'] += 1

                    # add state to the discard dataset
                    discard_count += 1
                    state = np.concatenate((
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
                    ), axis=1).astype(np.uint8)
                    filename = 'discard_' + year + '_' \
                               + str(discard_count) + '.png'
                    Image.fromarray(state * 255, 'L') \
                        .save(os.path.join(discard_dir, filename))

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
                    filename = 'discard_actions_' + year + '.txt'
                    with open(os.path.join(dataset_dir, filename), 'a') \
                            as f_discard:
                        f_discard.write(str(discarded_tile_converted) + '\n')

                    # update state
                    player_self.add_tile_to_hand(drawn_tile)
                    player_self.add_discard(discarded_tile)
                    player_self.riichi_status = True
                    player_self.riichi_turn_number = turn_number

                else:
                    # add action to the Riichi dataset
                    filename = 'riichi_actions_' + year + '.txt'
                    with open(os.path.join(dataset_dir, filename), 'a') \
                            as f_riichi:
                        f_riichi.write('0\n')
                    riichi_count['no'] += 1

                    # add state to the discard dataset
                    discard_count += 1
                    state = np.concatenate((
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
                    ), axis=1).astype(np.uint8)
                    filename = 'discard_' + year + '_' \
                               + str(discard_count) + '.png'
                    Image.fromarray(state * 255, 'L') \
                        .save(os.path.join(discard_dir, filename))

                    # add action to the discard dataset
                    discarded_tile = action
                    discarded_tile_converted = TENHOU_TILE_INDEX[discarded_tile]
                    if discarded_tile_converted == RED_FIVE_MAN:
                        discarded_tile_converted = FIVE_MAN
                    elif discarded_tile_converted == RED_FIVE_PIN:
                        discarded_tile_converted = FIVE_PIN
                    elif discarded_tile_converted == RED_FIVE_SOU:
                        discarded_tile_converted = FIVE_SOU
                    filename = 'discard_actions_' + year + '.txt'
                    with open(os.path.join(dataset_dir, filename), 'a') \
                            as f_discard:
                        f_discard.write(str(discarded_tile_converted) + '\n')

                    # update state
                    player_self.add_tile_to_hand(drawn_tile)
                    player_self.add_discard(discarded_tile)

            else:
                discarded_tile = action

                # if player hasn't declared Riichi, add data to the
                # discard dataset
                if not player_self.riichi_status:
                    discard_count += 1
                    state = np.concatenate((
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
                    ), axis=1).astype(np.uint8)
                    filename = 'discard_' + year + '_' \
                               + str(discard_count) + '.png'
                    Image.fromarray(state * 255, 'L') \
                        .save(os.path.join(discard_dir, filename))

                    discarded_tile_converted = TENHOU_TILE_INDEX[discarded_tile]
                    if discarded_tile_converted == RED_FIVE_MAN:
                        discarded_tile_converted = FIVE_MAN
                    elif discarded_tile_converted == RED_FIVE_PIN:
                        discarded_tile_converted = FIVE_PIN
                    elif discarded_tile_converted == RED_FIVE_SOU:
                        discarded_tile_converted = FIVE_SOU
                    filename = 'discard_actions_' + year + '.txt'
                    with open(os.path.join(dataset_dir, filename), 'a') \
                            as f_discard:
                        f_discard.write(str(discarded_tile_converted) + '\n')

                # update state
                player_self.add_tile_to_hand(drawn_tile)
                player_self.add_discard(discarded_tile)

        else:
            action = player_self.log_discards.popleft()
            if action == 60:
                action = drawn_tile
            discarded_tile = action
            remaining_discards -= 1

            # if player hasn't declared Riichi, add data to the discard dataset
            if not player_self.riichi_status:
                discard_count += 1
                state = np.concatenate((
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
                ), axis=1).astype(np.uint8)
                filename = 'discard_' + year + '_' \
                           + str(discard_count) + '.png'
                Image.fromarray(state * 255, 'L') \
                    .save(os.path.join(discard_dir, filename))

                discarded_tile_converted = TENHOU_TILE_INDEX[discarded_tile]
                if discarded_tile_converted == RED_FIVE_MAN:
                    discarded_tile_converted = FIVE_MAN
                elif discarded_tile_converted == RED_FIVE_PIN:
                    discarded_tile_converted = FIVE_PIN
                elif discarded_tile_converted == RED_FIVE_SOU:
                    discarded_tile_converted = FIVE_SOU
                filename = 'discard_actions_' + year + '.txt'
                with open(os.path.join(dataset_dir, filename), 'a') \
                        as f_discard:
                    f_discard.write(str(discarded_tile_converted) + '\n')

            # update state
            player_self.add_discard(discarded_tile)

        interrupted = False

        for i in range(3):
            if i != self_index \
                    and (not players[i].riichi_status) \
                    and players[i].log_draws:
                action = players[i].log_draws[0]
                if players[i].can_pon(discarded_tile):
                    # add state to the Pon dataset
                    pon_count['total'] += 1
                    state = np.concatenate((
                        encode_tile(discarded_tile),
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
                    ), axis=1).astype(np.uint8)
                    filename = 'pon_' + year + '_' \
                               + str(pon_count['total']) + '.png'
                    Image.fromarray(state * 255, 'L') \
                        .save(os.path.join(pon_dir, filename))

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
                            filename = 'pon_actions_' + year + '.txt'
                            with open(os.path.join(dataset_dir, filename), 'a') \
                                    as f_pon:
                                f_pon.write('1\n')
                            pon_count['yes'] += 1

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
                            filename = 'pon_actions_' + year + '.txt'
                            with open(os.path.join(dataset_dir, filename), 'a') \
                                    as f_pon:
                                f_pon.write('0\n')
                            pon_count['no'] += 1
                            is_pon = False
                            interrupted = False
                    else:
                        # add action to the Pon dataset
                        filename = 'pon_actions_' + year + '.txt'
                        with open(os.path.join(dataset_dir, filename), 'a') \
                                as f_pon:
                            f_pon.write('0\n')
                        pon_count['no'] += 1
                        is_pon = False
                        interrupted = False

                if players[i].can_open_kan(discarded_tile):
                    # add state to the Kan dataset
                    kan_count['total'] += 1
                    state = np.concatenate((
                        encode_tile(discarded_tile),
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
                    ), axis=1).astype(np.uint8)
                    filename = 'kan_' + year + '_' \
                               + str(kan_count['total']) + '.png'
                    Image.fromarray(state * 255, 'L') \
                        .save(os.path.join(kan_dir, filename))

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
                            filename = 'kan_actions_' + year + '.txt'
                            with open(os.path.join(dataset_dir, filename), 'a') \
                                    as f_kan:
                                f_kan.write('1\n')
                            kan_count['yes'] += 1

                            # update state
                            drawn_tile = discarded_tile
                            players[i].log_draws.popleft()
                            players[i].add_tile_to_hand(drawn_tile)
                            players[i].add_meld('kan', drawn_tile, turn_number)
                            dora_indicator_index += 1
                            encode_dora_indicator(dora_indicators, log[2],
                                                  dora_indicator_index)
                            if players[i].log_discards:
                                players[i].log_discards.popleft()
                                remaining_discards -= 1
                            self_index = i
                            is_pon = False
                            interrupted = True
                            break
                        else:
                            # add action to the Kan dataset
                            filename = 'kan_actions_' + year + '.txt'
                            with open(os.path.join(dataset_dir, filename), 'a') \
                                    as f_kan:
                                f_kan.write('0\n')
                            kan_count['no'] += 1
                            is_pon = False
                            interrupted = False
                    else:
                        # add action to the Kan dataset
                        filename = 'kan_actions_' + year + '.txt'
                        with open(os.path.join(dataset_dir, filename), 'a') \
                                as f_kan:
                            f_kan.write('0\n')
                        kan_count['no'] += 1
                        is_pon = False
                        interrupted = False

        if not interrupted:
            self_index = (self_index + 1) % 3
            is_pon = False

    return discard_count


def txt_to_csv(year, action_type):
    filename = action_type + '_actions_' + year
    with open(os.path.join(DATASET_PATH, filename + '.txt'), 'r') as txt_file:
        with open(os.path.join(DATASET_PATH, filename + '.csv'), 'w',
                  newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['image', 'label'])
            for index, line in enumerate(txt_file):
                image_name = action_type + '_' + year + '_' + \
                             str(index + 1) + '.png'
                writer.writerow([image_name, line[:-1]])


if __name__ == '__main__':
    assert False  # comment this line to confirm running the scripts

    # Extract game logs from the downloaded JSON objects
    pool = Pool(len(SELECTED_YEARS))
    for year in SELECTED_YEARS:
        pool.apply_async(extract_game_logs_from_json, args=(year,))
    pool.close()
    pool.join()

    # Count the number of extracted game logs
    total = 0
    for year in SELECTED_YEARS:
        count = count_extracted_game_logs(year)
        print(str(count) + ' game logs extracted from ' + year)
        total += count
    print('Total no. of game logs extracted: ' + str(total))

    # Find the maximum honba and deposit numbers
    max_honba_and_deposit_results = find_max_honba_and_deposit()
    for key, val in max_honba_and_deposit_results.items():
        print(key + ':', val)

    # Prepare images dataset for each action and year
    discard_count = 0
    pon_count = {
        'total': 0,
        'yes': 0,
        'no': 0
    }
    kan_count = {
        'total': 0,
        'yes': 0,
        'no': 0
    }
    kita_count = {
        'total': 0,
        'yes': 0,
        'no': 0
    }
    riichi_count = {
        'total': 0,
        'yes': 0,
        'no': 0
    }

    year = '2019'

    with tqdm(desc='Encoding', total=6000) as pbar:
        discard_dir = os.path.join(DATASET_PATH, 'discard_' + year)
        pon_dir = os.path.join(DATASET_PATH, 'pon_' + year)
        kan_dir = os.path.join(DATASET_PATH, 'kan_' + year)
        kita_dir = os.path.join(DATASET_PATH, 'kita_' + year)
        riichi_dir = os.path.join(DATASET_PATH, 'riichi_' + year)

        with open(os.path.join(EXTRACTED_GAME_LOGS_PATH, year + '.pickle'),
                  'rb') as fread:
            try:
                count = 0

                while log := pickle.load(fread):
                    count += 1

                    # (0-6000/30000 games)
                    if count <= 0:
                        continue
                    elif count > 6000:
                        break

                    if year == '2019' and count == 63813:
                        pbar.update(1)
                        continue
                    elif year == '2020' and count == 7628:
                        pbar.update(1)
                        continue

                    discard_count = encode_game_log(year=year,
                                                    log=log,
                                                    dataset_dir=DATASET_PATH,
                                                    discard_dir=discard_dir,
                                                    pon_dir=pon_dir,
                                                    kan_dir=kan_dir,
                                                    kita_dir=kita_dir,
                                                    riichi_dir=riichi_dir,
                                                    discard_count=discard_count,
                                                    pon_count=pon_count,
                                                    kan_count=kan_count,
                                                    kita_count=kita_count,
                                                    riichi_count=riichi_count)
                    pbar.update(1)
            except EOFError:
                pass
            except Exception:
                traceback.print_exc()
            finally:
                print()
                print('total discard data:', discard_count)
                print()
                print('total pon data:', pon_count['total'])
                print('pon accepted:', pon_count['yes'])
                print('pon declined:', pon_count['no'])
                print()
                print('total kan data:', kan_count['total'])
                print('kan accepted:', kan_count['yes'])
                print('kan declined:', kan_count['no'])
                print()
                print('total kita data:', kita_count['total'])
                print('kita accepted:', kita_count['yes'])
                print('kita declined:', kita_count['no'])
                print()
                print('total riichi data:', riichi_count['total'])
                print('riichi accepted:', riichi_count['yes'])
                print('riichi declined:', riichi_count['no'])

    # Validate .txt label (action) files
    for year in '2019', '2020':
        with open(os.path.join(DATASET_PATH,
                               'discard_actions_' + year + '.txt')) as f:
            assert len(list(map(int, f))) == DISCARD_COUNTS[year]
        with open(os.path.join(DATASET_PATH,
                               'pon_actions_' + year + '.txt')) as f:
            assert len(list(map(int, f))) == PON_COUNTS[year]['total']
        with open(os.path.join(DATASET_PATH,
                               'kan_actions_' + year + '.txt')) as f:
            assert len(list(map(int, f))) == KAN_COUNTS[year]['total']
        with open(os.path.join(DATASET_PATH,
                               'kita_actions_' + year + '.txt')) as f:
            assert len(list(map(int, f))) == KITA_COUNTS[year]['total']
        with open(os.path.join(DATASET_PATH,
                               'riichi_actions_' + year + '.txt')) as f:
            assert len(list(map(int, f))) == RIICHI_COUNTS[year]['total']

    # Convert .txt label (action) files to .csv files
    for year in '2019', '2020':
        for action_type in 'discard', 'pon', 'kan', 'kita', 'riichi':
            txt_to_csv(year=year, action_type=action_type)

    # Validate .csv label (action) files
    for year in '2019', '2020':
        with open(os.path.join(DATASET_PATH,
                               'discard_actions_' + year + '.csv')) as f:
            assert sum(1 for line in f) == DISCARD_COUNTS[year] + 1
        with open(os.path.join(DATASET_PATH,
                               'pon_actions_' + year + '.csv')) as f:
            assert sum(1 for line in f) == PON_COUNTS[year]['total'] + 1
        with open(os.path.join(DATASET_PATH,
                               'kan_actions_' + year + '.csv')) as f:
            assert sum(1 for line in f) == KAN_COUNTS[year]['total'] + 1
        with open(os.path.join(DATASET_PATH,
                               'kita_actions_' + year + '.csv')) as f:
            assert sum(1 for line in f) == KITA_COUNTS[year]['total'] + 1
        with open(os.path.join(DATASET_PATH,
                               'riichi_actions_' + year + '.csv')) as f:
            assert sum(1 for line in f) == RIICHI_COUNTS[year]['total'] + 1
