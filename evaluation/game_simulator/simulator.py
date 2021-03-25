import numpy as np
from collections import deque

from typing import List

from data_processing.data_preprocessing_constants import SCORES_SIZE, \
    ONE_SCORE_SIZE, \
    DORA_INDICATORS_SIZE
from evaluation.agents.agent import Agent
from evaluation.agents.random_agent import RandomAgent
from evaluation.hand_calculation.hand_config import HandConfig
from evaluation.hand_calculation.tile_constants import TILES_COUNT, TWO_MAN, \
    FIVE_MAN, NINE_MAN, FIVE_PIN, FIVE_SOU, EAST, SOUTH, WEST, NORTH, \
    RED_FIVE_MAN, RED_FIVE_PIN, RED_FIVE_SOU, YAOCHUUHAI


def encode_tile(tile):
    """
    :param tenhou_encoded_tile: integer index of a tile
    :return: (34, 1) np.array
    """
    output = np.zeros((34, 1))

    if tile == RED_FIVE_MAN:
        tile = FIVE_MAN
    elif tile == RED_FIVE_PIN:
        tile = FIVE_PIN
    elif tile == RED_FIVE_SOU:
        tile = FIVE_SOU

    output[tile, :] = 1
    return output


def encode_scores(scores):
    """
    :param scores: list of all 4 player's scores (even for 3-player Mahjong)
    :return: (34, 44) np.array
    """
    output = np.zeros((34, SCORES_SIZE))
    for index, score in enumerate(scores):
        for bit, val in enumerate(bin(score // 100)[2:].zfill(ONE_SCORE_SIZE)):
            if val == '1':
                output[:, index * ONE_SCORE_SIZE + bit] = 1
    return output


def update_dora_indicators(dora_indicators, tile, index):
    """
    :param dora_indicators: (34, 4) np.array, original encoded dora indicators
    :param tile: list of dora indicators
    :param index: index of the dora indicator
    :return: updated (34, 4) np.array
    """
    if tile == RED_FIVE_MAN:
        dora_indicators[FIVE_MAN, index] = 1
    elif tile == RED_FIVE_PIN:
        dora_indicators[FIVE_PIN, index] = 1
    elif tile == RED_FIVE_SOU:
        dora_indicators[FIVE_SOU, index] = 1
    else:
        dora_indicators[tile, index] = 1


def shuffle(seed=None):
    """
    :param seed: The NumPy random seed.
    :return: np.array
    """
    if seed is not None:
        np.random.seed(seed)
    wall = np.random.permutation(np.delete(
        np.arange(TILES_COUNT * 4), np.arange(TWO_MAN * 4, NINE_MAN * 4)))
    wall[wall == FIVE_MAN * 4] = RED_FIVE_MAN * 4
    wall[wall == FIVE_PIN * 4] = RED_FIVE_PIN * 4
    wall[wall == FIVE_SOU * 4] = RED_FIVE_SOU * 4
    return wall // 4


def deal(wall, player_east, player_south, player_west):
    """
    :param wall: np.array
    :param player_east: Agent
    :param player_south: Agent
    :param player_west: Agent
    """
    player_east_hand = np.hstack(
        (wall[0:4], wall[12:16], wall[24:28], wall[36]))
    player_south_hand = np.hstack(
        (wall[4:8], wall[16:20], wall[28:32], wall[37]))
    player_west_hand = np.hstack(
        (wall[8:12], wall[20:24], wall[32:36], wall[38]))
    player_east.encode_start_hand(sorted(player_east_hand))
    player_south.encode_start_hand(sorted(player_south_hand))
    player_west.encode_start_hand(sorted(player_west_hand))


def simulate(players: List[Agent], round_number=0, honba_number=0,
             deposit_number=0,
             seed=None):
    """
    :param players: list of Agent
    :param round_number: integer
    :param honba_number: integer
    :param deposit_number: integer
    :param seed: integer
    """
    scores = encode_scores([
        players[0].score, players[1].score, players[2].score, 0
    ])
    hand_configs = [
        HandConfig(is_sanma=True, seat_wind=EAST, honba_counter=honba_number),
        HandConfig(is_sanma=True, seat_wind=SOUTH, honba_counter=honba_number),
        HandConfig(is_sanma=True, seat_wind=WEST, honba_counter=honba_number)
    ]
    player_hand_config_dict = {
        players[0]: hand_configs[0],
        players[1]: hand_configs[1],
        players[2]: hand_configs[2]
    }

    wall = shuffle(seed)
    deal(wall, players[0], players[1], players[2])
    wall = deque(wall[39:])
    dora_indicators = np.zeros((TILES_COUNT, DORA_INDICATORS_SIZE))
    possible_dora_indicators = [wall[-6], wall[-8], wall[-10], wall[-12]]
    possible_uradora_indicators = [wall[-5], wall[-7], wall[-9], wall[-11]]
    update_dora_indicators(dora_indicators, possible_dora_indicators[0], 0)

    east_index = 0
    self_index = east_index
    turn_number = 0
    kan_count = 0
    is_pon = False
    end_game = False
    is_ron = False
    is_tsumo = False
    is_ryuukyoku = False
    win_tile = -1
    win_players = []
    lose_player = -1

    while len(wall) > 14 or not end_game:
        if self_index == east_index:
            turn_number += 1

        player_self = players[self_index]
        player1 = players[(self_index + 1) % 3]
        player2 = players[(self_index + 2) % 3]
        player3 = RandomAgent()

        if not is_pon:
            draw_flag = True
            drawn_tile = wall.popleft()
            final_action = 'skip'

            while draw_flag:
                draw_flag = False
                max_confidence = -1.0
                final_action = 'skip'

                ################################################################

                if player_self.can_win(drawn_tile):
                    win_decision = player_self.eval_win(
                        drawn_tile, player1, player2, player3,
                        scores, round_number, honba_number,
                        deposit_number, dora_indicators)
                    if win_decision > 0.5:
                        end_game = True
                        is_tsumo = True
                        win_players.append(player_self)
                        win_tile = drawn_tile
                        win_hand_config = hand_configs[self_index]
                        win_hand_config.deposit_counter = deposit_number
                        win_hand_config.is_tsumo = True
                        if turn_number == 1:
                            if player_self.discard_index == 0 \
                                    and not player_self.naki_status:
                                win_hand_config.is_menzen = True
                                if self_index == east_index:
                                    win_hand_config.is_tenhou = True
                                else:
                                    if not player1.naki_status \
                                            and not player2.naki_status:
                                        win_hand_config.is_chiihou = True
                        else:
                            if player_self.double_riichi_status:
                                win_hand_config.is_double_riichi = True
                            elif player_self.riichi_status:
                                win_hand_config.is_riichi = True

                            if not player_self.pon_tiles \
                                    and not player_self.open_kan:
                                win_hand_config.is_menzen = True

                            if final_action == 'closed_kan' or 'add_kan' \
                                    or 'kita':
                                win_hand_config.is_rinshan = True
                            elif len(wall) == 14:
                                win_hand_config.is_haitei = True

                ################################################################

                closed_kan_tile, can_closed_kan = player_self.can_closed_kan(
                    kan_count, len(wall) - 14, drawn_tile)
                if can_closed_kan:
                    kan_decision = player_self.eval_kan(
                        drawn_tile, player1, player2, player3, scores,
                        round_number, honba_number, deposit_number,
                        dora_indicators)
                    if kan_decision > 0.5:
                        if kan_decision > max_confidence:
                            max_confidence = kan_decision
                            final_action = 'closed_kan'

                add_kan_tile, can_add_kan = player_self.can_add_kan(
                    kan_count, len(wall) - 14, drawn_tile)
                if can_add_kan:
                    kan_decision = player_self.eval_kan(
                        drawn_tile, player1, player2, player3, scores,
                        round_number, honba_number, deposit_number,
                        dora_indicators)
                    if kan_decision > 0.5:
                        if kan_decision > max_confidence:
                            max_confidence = kan_decision
                            final_action = 'add_kan'

                if player_self.can_kita(len(wall) - 14, drawn_tile):
                    kita_decision = player_self.eval_kita(
                        drawn_tile, player1, player2, player3, scores,
                        round_number, honba_number, deposit_number,
                        dora_indicators)
                    if kita_decision > 0.5:
                        if kita_decision > max_confidence:
                            max_confidence = kita_decision
                            final_action = 'kita'

                ################################################################

                if final_action == 'closed_kan':
                    draw_flag = True
                    player_self.add_tile_to_hand(drawn_tile)
                    player_self.make_closed_kan(closed_kan_tile, turn_number)
                    if closed_kan_tile in YAOCHUUHAI:
                        for i in (self_index + 1) % 3, (self_index + 2) % 3:
                            player = players[i]
                            if i == (self_index + 1) % 3:
                                next_player = player2
                                prev_player = player_self
                            else:  # if i == (self_index + 2) % 3:
                                next_player = player_self
                                prev_player = player1

                            if player.can_kokushi_musou(closed_kan_tile):
                                win_decision = player_self.eval_win(
                                    closed_kan_tile, next_player, prev_player,
                                    player3, scores, round_number, honba_number,
                                    deposit_number, dora_indicators)
                                if win_decision > 0.5:
                                    end_game = True
                                    is_ron = True
                                    win_players.append(player)
                                    lose_player = player_self
                                    win_tile = closed_kan_tile
                                    win_hand_config = hand_configs[i]
                                    win_hand_config.deposit_counter = deposit_number
                                    win_hand_config.is_chankan = True

                                    if player_self.double_riichi_status:
                                        win_hand_config.is_double_riichi = True
                                    elif player_self.riichi_status:
                                        win_hand_config.is_riichi = True

                                    if not player_self.pon_tiles \
                                            and not player_self.open_kan:
                                        win_hand_config.is_menzen = True

                    if not end_game:
                        kan_count += 1
                        if kan_count == 4 \
                                and len(player_self.open_kan) \
                                + len(player_self.closed_kan) != 4:
                            end_game = True
                            is_ryuukyoku = True
                        else:
                            update_dora_indicators(
                                dora_indicators,
                                possible_dora_indicators[kan_count], kan_count)
                            drawn_tile = wall.pop()

                elif final_action == 'add_kan':
                    draw_flag = True
                    player_self.add_tile_to_hand(drawn_tile)
                    player_self.make_added_kan(add_kan_tile, turn_number)
                    for i in (self_index + 1) % 3, (self_index + 2) % 3:
                        player = players[i]
                        if i == (self_index + 1) % 3:
                            next_player = player2
                            prev_player = player_self
                        else:  # if i == (self_index + 2) % 3:
                            next_player = player_self
                            prev_player = player1

                        if player.can_win(add_kan_tile):
                            win_decision = player_self.eval_win(
                                add_kan_tile, next_player, prev_player,
                                player3, scores, round_number, honba_number,
                                deposit_number, dora_indicators)
                            if win_decision > 0.5:
                                end_game = True
                                is_ron = True
                                win_players.append(player)
                                lose_player = player_self
                                win_tile = add_kan_tile
                                win_hand_config = hand_configs[i]
                                win_hand_config.deposit_counter = deposit_number
                                win_hand_config.is_chankan = True

                                if player_self.double_riichi_status:
                                    win_hand_config.is_double_riichi = True
                                elif player_self.riichi_status:
                                    win_hand_config.is_riichi = True

                                if not player_self.pon_tiles \
                                        and not player_self.open_kan:
                                    win_hand_config.is_menzen = True

                    if not end_game:
                        kan_count += 1
                        if kan_count == 4 \
                                and len(player_self.open_kan) \
                                + len(player_self.closed_kan) != 4:
                            end_game = True
                            is_ryuukyoku = True
                        else:
                            drawn_tile = wall.pop()

                elif final_action == 'kita':
                    draw_flag = True
                    player_self.add_tile_to_hand(drawn_tile)
                    player_self.add_kita()
                    for i in (self_index + 1) % 3, (self_index + 2) % 3:
                        player = players[i]
                        if i == (self_index + 1) % 3:
                            next_player = player2
                            prev_player = player_self
                        else:  # if i == (self_index + 2) % 3:
                            next_player = player_self
                            prev_player = player1

                        if player.can_win(NORTH):
                            win_decision = player_self.eval_win(
                                NORTH, next_player, prev_player, player3,
                                scores, round_number, honba_number,
                                deposit_number, dora_indicators)
                            if win_decision > 0.5:
                                end_game = True
                                is_ron = True
                                win_players.append(player)
                                lose_player = player_self
                                win_tile = NORTH
                                win_hand_config = hand_configs[i]
                                win_hand_config.deposit_counter = deposit_number

                                if player_self.double_riichi_status:
                                    win_hand_config.is_double_riichi = True
                                elif player_self.riichi_status:
                                    win_hand_config.is_riichi = True

                                if not player_self.pon_tiles \
                                        and not player_self.open_kan:
                                    win_hand_config.is_menzen = True

                else:  # if final_action == 'skip':
                    player_self.add_tile_to_hand(drawn_tile)
                    draw_flag = False

                if end_game:
                    break

            if end_game:
                break

            if player_self.can_riichi(drawn_tile):
                riichi_decision = player_self.eval_riichi(
                    drawn_tile, player1, player2, player3, scores,
                    round_number, honba_number, deposit_number,
                    dora_indicators)
                if riichi_decision > 0.5:
                    player_self.riichi_status = True
                    player_self.riichi_turn_number = turn_number

            discarded_tile = player_self.eval_riichi(
                drawn_tile, player1, player2, player3, scores,
                round_number, honba_number, deposit_number,
                dora_indicators)
            player_self.add_discard(discarded_tile)
            if final_action == 'add_kan':
                update_dora_indicators(dora_indicators,
                                       possible_dora_indicators[kan_count],
                                       kan_count)

        else:
            discarded_tile = player_self.eval_riichi(
                drawn_tile, player1, player2, player3, scores,
                round_number, honba_number, deposit_number,
                dora_indicators)
            player_self.add_discard(discarded_tile)

        interrupted = False

        for i in (self_index + 1) % 3, (self_index + 2) % 3:
            player = players[i]
            if i == (self_index + 1) % 3:
                next_player = player2
                prev_player = player_self
            else:  # if i == (self_index + 2) % 3:
                next_player = player_self
                prev_player = player1

            if player.can_win(discarded_tile):
                win_decision = player.eval_win(
                    discarded_tile, next_player, prev_player, player3, scores,
                    round_number, honba_number, deposit_number,
                    dora_indicators)
                if win_decision > 0.5:
                    end_game = True
                    is_ron = True
                    win_players.append(player)
                    lose_player = player_self
                    win_tile = discarded_tile
                    win_hand_config = hand_configs[i]
                    win_hand_config.deposit_counter = deposit_number

                    if player_self.double_riichi_status:
                        win_hand_config.is_double_riichi = True
                    elif player_self.riichi_status:
                        win_hand_config.is_riichi = True

                    if not player_self.pon_tiles \
                            and not player_self.open_kan:
                        win_hand_config.is_menzen = True

                    if len(wall) == 14:
                        win_hand_config.is_houtei = True

            if player.can_open_kan(kan_count, len(wall) - 14, discarded_tile):
                kan_decision = player.eval_kan(
                    discarded_tile, next_player, prev_player, player3, scores,
                    round_number, honba_number, deposit_number,
                    dora_indicators)
                if kan_decision > 0.5:
                    drawn_tile = discarded_tile
                    player.add_tile_to_hand(drawn_tile)
                    player.make_open_kan(drawn_tile, turn_number)
                    self_index = i
                    is_pon = False
                    interrupted = True

                    for j, chankan_player in next_player, prev_player:
                        if j == 0:
                            chankan_next_player = prev_player
                            chankan_prev_player = player
                        else:
                            chankan_next_player = player
                            chankan_prev_player = next_player

                        if chankan_player.can_win(drawn_tile):
                            win_decision = chankan_player.eval_win(
                                drawn_tile, chankan_next_player,
                                chankan_prev_player, player3, scores,
                                round_number, honba_number, deposit_number,
                                dora_indicators)
                            if win_decision > 0.5:
                                end_game = True
                                is_ron = True
                                win_players.append(chankan_player)
                                lose_player.append(player)
                                win_tile = drawn_tile
                                win_hand_config = player_hand_config_dict[chankan_player]
                                win_hand_config.deposit_counter = deposit_number
                                win_hand_config.is_chankan = True

                                if player_self.double_riichi_status:
                                    win_hand_config.is_double_riichi = True
                                elif player_self.riichi_status:
                                    win_hand_config.is_riichi = True

                                if not player_self.pon_tiles \
                                        and not player_self.open_kan:
                                    win_hand_config.is_menzen = True

                    if not end_game:
                        kan_count += 1
                        if kan_count == 4 \
                                and len(player_self.open_kan) \
                                + len(player_self.closed_kan) != 4:
                            end_game = True
                            is_ryuukyoku = True
                        else:
                            update_dora_indicators(
                                dora_indicators,
                                possible_dora_indicators[kan_count], kan_count)
                            drawn_tile = wall.pop()
                else:
                    is_pon = False
                    interrupted = False

            if player.can_pon(discarded_tile):
                pon_decision = player.eval_pon(
                    discarded_tile, next_player, prev_player, player3, scores,
                    round_number, honba_number, deposit_number,
                    dora_indicators)
                if pon_decision > 0.5:
                    drawn_tile = discarded_tile
                    player.add_tile_to_hand(drawn_tile)
                    player.make_pon(drawn_tile, turn_number)
                    self_index = i
                    is_pon = True
                    interrupted = True
                    break
                else:
                    is_pon = False
                    interrupted = False
            else:
                is_pon = False
                interrupted = False

        if not end_game or not interrupted:
            self_index = (self_index + 1) % 3
            is_pon = False

    # TODO: finish score calculation


if __name__ == '__main__':
    a = 'a'
    b = 'b'
    for i, c in enumerate([a,b]):
        print(i, c)
