from itertools import product
from abc import ABC, abstractmethod

import numpy as np

from data_processing.data_processing_constants import TILES_SIZE, \
    SELF_RED_DORA_SIZE, MELDS_SIZE, KITA_SIZE, DISCARDS_SIZE, ONE_MELD_SIZE, \
    TURN_NUMBER_SIZE, ROUND_NUMBER_SIZE, HONBA_NUMBER_SIZE, DEPOSIT_NUMBER_SIZE
from evaluation.hand_calculation.han import Han
from evaluation.hand_calculation.hand_calculator import HandCalculator
from evaluation.hand_calculation.hand_config import HandConfig
from evaluation.hand_calculation.hand_divider import HandDivider
from evaluation.hand_calculation.meld import Meld
from evaluation.hand_calculation.riichi_checker import RiichiChecker
from evaluation.hand_calculation.tenpai import Tenpai
from evaluation.hand_calculation.tile_constants import ONE_MAN, FIVE_MAN, \
    NINE_MAN, ONE_PIN, FIVE_PIN, NINE_PIN, ONE_SOU, FIVE_SOU, NINE_SOU, EAST, \
    NORTH, CHUN, RED_FIVE_MAN, RED_FIVE_PIN, RED_FIVE_SOU, YAOCHUUHAI
from evaluation.hand_calculation.tiles import Tiles


class Agent(ABC):
    def __init__(self, wind=None, score=35000):
        self.hand = np.zeros((34, TILES_SIZE))
        self.red_dora = np.zeros((34, SELF_RED_DORA_SIZE))
        self.melds = np.zeros((34, MELDS_SIZE))
        self.kita = np.zeros((34, KITA_SIZE))
        self.kita_count = 0
        self.discards = np.zeros((34, DISCARDS_SIZE))
        self.discard_index = 0
        self.discard_tiles = []
        self.meld_tiles = []
        self.pon_tiles = []
        self.open_kan = []
        self.closed_kan = []
        self.riichi_status = False
        self.double_riichi_status = False
        self.riichi_turn_number = 0
        self.naki_status = False
        self.wind = wind
        self.score = score

    def reset(self, wind=None, score=35000):
        self.hand = np.zeros((34, TILES_SIZE))
        self.red_dora = np.zeros((34, SELF_RED_DORA_SIZE))
        self.melds = np.zeros((34, MELDS_SIZE))
        self.kita = np.zeros((34, KITA_SIZE))
        self.kita_count = 0
        self.discards = np.zeros((34, DISCARDS_SIZE))
        self.discard_index = 0
        self.discard_tiles = []
        self.meld_tiles = []
        self.pon_tiles = []
        self.open_kan = []
        self.closed_kan = []
        self.riichi_status = False
        self.double_riichi_status = False
        self.riichi_turn_number = 0
        self.naki_status = False
        self.wind = wind
        self.score = score

    def set_wind(self, wind):
        self.wind = wind

    def set_score(self, score):
        self.score = score

    @staticmethod
    def encode_tile(tile):
        """
        :param tile: Integer index of a tile
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

    @staticmethod
    def encode_number(number, size):
        """
        :param number: Integer
        :return: (34, size) np.array
        """
        output = np.empty((34, size))
        for bit, val in enumerate(bin(number)[2:].zfill(size)):
            if val == '1':
                output[:, bit] = 1
            else:
                output[:, bit] = 0
        return output

    @staticmethod
    def encode_turn_number(turn_number):
        """
        :param turn_number: integer
        :return: (34, 5) np.array
        """
        return Agent.encode_number(turn_number, TURN_NUMBER_SIZE)

    @staticmethod
    def encode_round_number(round_number):
        """
        :param round_number: integer
        :return: (34, 3) np.array
        """
        return Agent.encode_number(round_number, ROUND_NUMBER_SIZE)

    @staticmethod
    def encode_honba_number(honba_number):
        """
        :param honba_number: integer
        :return: (34, 4) np.array
        """
        return Agent.encode_number(honba_number, HONBA_NUMBER_SIZE)

    @staticmethod
    def encode_deposit_number(deposit_number):
        """
        :param deposit_number: integer
        :return: (34, 4) np.array
        """
        return Agent.encode_number(deposit_number, DEPOSIT_NUMBER_SIZE)

    def encode_riichi_status(self):
        if self.riichi_status:
            riichi_status_encoded = np.ones((34, 1))
        else:
            riichi_status_encoded = np.zeros((34, 1))

        return np.concatenate((
            riichi_status_encoded,
            Agent.encode_turn_number(self.riichi_turn_number)
        ), axis=1)

    def can_pon(self, target_tile):
        """
        :param target_tile: Integer index of a tile
        :return: Boolean
        """
        if self.riichi_status:
            return False

        if target_tile == RED_FIVE_MAN:
            target_tile = FIVE_MAN
        elif target_tile == RED_FIVE_PIN:
            target_tile = FIVE_PIN
        elif target_tile == RED_FIVE_SOU:
            target_tile = FIVE_SOU

        return np.sum(self.hand[target_tile], dtype=np.int32) >= 2

    def can_closed_kan(self, kan_count, remaining_tiles, target_tile):
        """
        :param kan_count: Integer count of all kan
        :param remaining_tiles: Integer count of remaining tiles
        :param target_tile: Integer index of a tile
        :return: (integer, Boolean)
        """
        if kan_count == 4 or remaining_tiles == 0:
            return -1, False

        if target_tile == RED_FIVE_MAN:
            target_tile = FIVE_MAN
        elif target_tile == RED_FIVE_PIN:
            target_tile = FIVE_PIN
        elif target_tile == RED_FIVE_SOU:
            target_tile = FIVE_SOU

        if np.sum(self.hand[target_tile], dtype=np.int32) == 3 \
                or 4 in self.hand.sum(axis=1):
            if np.sum(self.hand[target_tile], dtype=np.int32) == 3:
                kan_tile = target_tile
            else:  # if 4 in self.hand.sum(axis=1):
                kan_tile = np.where(self.hand.sum(axis=1) == 4)[0][0]

            if not self.riichi_status:
                return kan_tile, True
            else:
                tiles = Tiles.matrix_to_array(self.hand)
                # manzu
                man = RiichiChecker.find_combinations(tiles, ONE_MAN, NINE_MAN)
                # pinzu
                pin = RiichiChecker.find_combinations(tiles, ONE_PIN, NINE_PIN)
                # souzu
                sou = RiichiChecker.find_combinations(tiles, ONE_SOU, NINE_SOU)
                # honours
                honours = RiichiChecker.find_combinations(tiles, EAST, CHUN)

                combinations_sets = [[]]
                if man:
                    combinations_sets.append(man)
                if pin:
                    combinations_sets.append(pin)
                if sou:
                    combinations_sets.append(sou)
                if honours:
                    combinations_sets.append(honours)
                combinations_sets.pop(0)

                for combinations in product(*combinations_sets):
                    has_koutsu = False
                    mentsu_count = 0
                    pair_count = 0
                    taatsu_count = 0
                    singleton_count = 0

                    if self.closed_kan:
                        mentsu_count += len(self.closed_kan)

                    for combination in list(combinations):
                        for item in combination:
                            if len(item) == 3:
                                mentsu_count += 1
                                if item[0] == item[1] == item[2] == target_tile:
                                    has_koutsu = True
                            elif len(item) == 2:
                                if item[0] == item[1]:
                                    pair_count += 1
                                else:
                                    taatsu_count += 1
                            else:  # len(item) == 1
                                singleton_count += 1

                    counts = (mentsu_count, pair_count, taatsu_count,
                              singleton_count)
                    if counts == (4, 0, 0, 1) \
                            or counts == (3, 2, 0, 0) \
                            or counts == (3, 1, 1, 0):
                        if has_koutsu:
                            return kan_tile, True

                return -1, False
        else:
            return -1, False

    def can_open_kan(self, kan_count, remaining_tiles, target_tile):
        """
        :param kan_count: Integer count of all kan
        :param remaining_tiles: Integer count of remaining tiles
        :param target_tile: Integer index of a tile
        :return: Boolean
        """
        if kan_count == 4 or remaining_tiles == 0 or self.riichi_status:
            return False

        if target_tile == RED_FIVE_MAN:
            target_tile = FIVE_MAN
        elif target_tile == RED_FIVE_PIN:
            target_tile = FIVE_PIN
        elif target_tile == RED_FIVE_SOU:
            target_tile = FIVE_SOU

        return np.sum(self.hand[target_tile], dtype=np.int32) == 3

    def can_add_kan(self, kan_count, remaining_tiles, target_tile):
        """
        :param kan_count: Integer count of all kan
        :param remaining_tiles: Integer count of remaining tiles
        :param target_tile: Integer index of a tile
        :return: (integer, Boolean)
        """
        if kan_count == 4 or remaining_tiles == 0 or self.riichi_status:
            return -1, False

        if target_tile == RED_FIVE_MAN:
            target_tile = FIVE_MAN
        elif target_tile == RED_FIVE_PIN:
            target_tile = FIVE_PIN
        elif target_tile == RED_FIVE_SOU:
            target_tile = FIVE_SOU

        for meld in self.meld_tiles:
            if meld == target_tile or self.hand[meld, 0] == 1:
                return meld, True
        return -1, False

    def can_kita(self, remaining_tiles, target_tile):
        """
        :param remaining_tiles: Integer count of remaining tiles
        :param target_tile: Integer index of a tile
        :return: Boolean
        """
        if remaining_tiles == 0:
            return False

        if self.riichi_status:
            return target_tile == NORTH
        else:
            return target_tile == NORTH \
                   or np.sum(self.hand[NORTH], dtype=np.int32) > 0

    def can_riichi(self, target_tile):
        """
        :param target_tile: Integer index of a tile
        :return: Boolean
        """
        if self.riichi_status or self.pon_tiles or self.open_kan \
                or self.score < 1000:
            return False

        if target_tile == RED_FIVE_MAN:
            target_tile = FIVE_MAN
        elif target_tile == RED_FIVE_PIN:
            target_tile = FIVE_PIN
        elif target_tile == RED_FIVE_SOU:
            target_tile = FIVE_SOU

        private_tiles_array = Tiles.matrix_to_array(self.hand)

        return RiichiChecker.can_riichi(private_tiles_array, target_tile,
                                        self.closed_kan)

    def has_kyuushu_kyuuhai(self, target_tile, player1, player2, player3=None):
        yaochuuhai_count = np.sum(self.hand[YAOCHUUHAI, 0], dtype=np.int32)
        if target_tile in YAOCHUUHAI and self.hand[target_tile, 0] == 0:
            yaochuuhai_count += 1

        if player3 is not None:
            return yaochuuhai_count >= 9 and \
                   not (self.naki_status or player1.naki_status
                        or player2.naki_status or player3.naki_status)
        else:
            return yaochuuhai_count >= 9 and \
                   not (self.naki_status or player1.naki_status
                        or player2.naki_status)

    def is_tenpai(self):
        private_tiles_array = Tiles.matrix_to_array(self.hand)

        meld_objects = []
        for pon_tile in self.pon_tiles:
            meld_objects.append(Meld(
                meld_type=Meld.PON,
                tiles=Tiles.indices_to_array([pon_tile] * 3)
            ))
        for kan_tile in self.open_kan:
            meld_objects.append(Meld(
                meld_type=Meld.KAN,
                tiles=Tiles.indices_to_array([kan_tile] * 4)
            ))
        for kan_tile in self.closed_kan:
            meld_objects.append(Meld(
                meld_type=Meld.KAN,
                tiles=Tiles.indices_to_array([kan_tile] * 4),
                is_open=False
            ))

        tenpai = Tenpai.calculate_tenpai(private_tiles_array, meld_objects)
        return len(tenpai) > 0

    def can_win(self, target_tile):
        """
        :param target_tile: Integer index of a tile
        :return: Boolean
        """
        if target_tile == RED_FIVE_MAN:
            target_tile = FIVE_MAN
        elif target_tile == RED_FIVE_PIN:
            target_tile = FIVE_PIN
        elif target_tile == RED_FIVE_SOU:
            target_tile = FIVE_SOU

        if target_tile in self.discard_tiles:
            return False

        private_tiles_array = Tiles.matrix_to_array(self.hand)

        meld_objects = []
        for pon_tile in self.pon_tiles:
            meld_objects.append(Meld(
                meld_type=Meld.PON,
                tiles=Tiles.indices_to_array([pon_tile] * 3)
            ))
        for kan_tile in self.open_kan:
            meld_objects.append(Meld(
                meld_type=Meld.KAN,
                tiles=Tiles.indices_to_array([kan_tile] * 4)
            ))
        for kan_tile in self.closed_kan:
            meld_objects.append(Meld(
                meld_type=Meld.KAN,
                tiles=Tiles.indices_to_array([kan_tile] * 4),
                is_open=False
            ))

        hand_options = HandDivider.divide_hand(
            private_tiles=private_tiles_array,
            win_tile=target_tile,
            melds=meld_objects
        )
        hand_config = HandConfig()

        # Kokushi Musou
        if isinstance(hand_options[0], int):
            if (hand_config.yaku.kokushi_musou.is_condition_met(
                    hand_options)
                    or hand_config.yaku.kokushi_musou_13_men.is_condition_met(
                        hand_options, target_tile)):
                return True
            else:
                return False
        # Other winning cases
        else:
            for hand in hand_options:
                win_group_options = HandCalculator.find_all_win_groups(
                    hand=hand,
                    win_tile=target_tile,
                    melds=meld_objects)

                for win_group in win_group_options:
                    han_details, han, is_yakuman = Han.calculate_han(
                        hand=hand,
                        win_tile=target_tile,
                        win_group=win_group,
                        melds=meld_objects,
                        hand_config=hand_config
                    )

                    for han_detail in han_details:
                        if han_detail['reason'] == Han.DORA \
                                or han_detail['reason'] == Han.RED_DORA \
                                or han_detail['reason'] == Han.NUKI_DORA:
                            han -= han_detail['han']

                    if han > 0 or is_yakuman:
                        return True

            return False

    def can_kokushi_musou(self, target_tile):
        """
        :param target_tile: Integer index of a tile
        :return: Boolean
        """
        if target_tile == RED_FIVE_MAN:
            target_tile = FIVE_MAN
        elif target_tile == RED_FIVE_PIN:
            target_tile = FIVE_PIN
        elif target_tile == RED_FIVE_SOU:
            target_tile = FIVE_SOU

        private_tiles_array = Tiles.matrix_to_array(self.hand)

        meld_objects = []
        for pon_tile in self.pon_tiles:
            meld_objects.append(Meld(
                meld_type=Meld.PON,
                tiles=Tiles.indices_to_array([pon_tile] * 3)
            ))
        for kan_tile in self.open_kan:
            meld_objects.append(Meld(
                meld_type=Meld.KAN,
                tiles=Tiles.indices_to_array([kan_tile] * 4)
            ))
        for kan_tile in self.closed_kan:
            meld_objects.append(Meld(
                meld_type=Meld.KAN,
                tiles=Tiles.indices_to_array([kan_tile] * 4),
                is_open=False
            ))

        hand_options = HandDivider.divide_hand(
            private_tiles=private_tiles_array,
            win_tile=target_tile,
            melds=meld_objects
        )
        hand_config = HandConfig()

        # Kokushi Musou
        if isinstance(hand_options[0], int):
            if (hand_config.yaku.kokushi_musou.is_condition_met(
                    hand_options)
                    or hand_config.yaku.kokushi_musou_13_men.is_condition_met(
                        hand_options, target_tile)):
                return True
            else:
                return False
        else:
            return False

    def add_tile_to_hand(self, tile):
        """
        :param tile: integer index of a tile
        """
        if tile == RED_FIVE_MAN:
            index = 0
            while self.hand[FIVE_MAN, index] != 0:
                index += 1
            self.hand[FIVE_MAN, index] = 1
            self.red_dora[FIVE_MAN] = 1
        elif tile == RED_FIVE_PIN:
            index = 0
            while self.hand[FIVE_PIN, index] != 0:
                index += 1
            self.hand[FIVE_PIN, index] = 1
            self.red_dora[FIVE_PIN] = 1
        elif tile == RED_FIVE_SOU:
            index = 0
            while self.hand[FIVE_SOU, index] != 0:
                index += 1
            self.hand[FIVE_SOU, index] = 1
            self.red_dora[FIVE_SOU] = 1
        else:
            converted_tile = tile
            index = 0
            while self.hand[converted_tile, index] != 0:
                index += 1
            self.hand[converted_tile, index] = 1

    def discard_tile_from_hand(self, tile):
        """
        :param tile: integer index of a tile
        """
        if tile == RED_FIVE_MAN:
            index = 0
            while index < 4 and self.hand[FIVE_MAN, index] != 0:
                index += 1
            self.hand[FIVE_MAN, index - 1] = 0
            self.red_dora[FIVE_MAN] = 0
        elif tile == RED_FIVE_PIN:
            index = 0
            while index < 4 and self.hand[FIVE_PIN, index] != 0:
                index += 1
            self.hand[FIVE_PIN, index - 1] = 0
            self.red_dora[FIVE_PIN] = 0
        elif tile == RED_FIVE_SOU:
            index = 0
            while index < 4 and self.hand[FIVE_SOU, index] != 0:
                index += 1
            self.hand[FIVE_SOU, index - 1] = 0
            self.red_dora[FIVE_SOU] = 0
        else:
            converted_tile = tile
            index = 0
            while index < 4 and self.hand[converted_tile, index] != 0:
                index += 1
            self.hand[converted_tile, index - 1] = 0

    def add_discard(self, tile):
        """
        :param tile: integer index of a tile
        """
        if tile == RED_FIVE_MAN:
            tile = FIVE_MAN
        elif tile == RED_FIVE_PIN:
            tile = FIVE_PIN
        elif tile == RED_FIVE_SOU:
            tile = FIVE_SOU

        self.discard_tiles.append(tile)
        self.discards[tile, self.discard_index] = 1
        self.discard_index += 1
        self.discard_tile_from_hand(tile)

    def add_kita(self):
        self.naki_status = True
        self.kita[NORTH, self.kita_count] = 1
        self.kita_count += 1
        self.discard_tile_from_hand(NORTH)

    def __add_meld(self, meld_type, tile, turn_number):
        """
        :param meld_type: String, 'pon' or 'kan'
        :param tile: integer index of a tile
        :param turn_number: Integer
        """
        self.naki_status = True
        meld_index = len(self.meld_tiles) + 1
        if tile == RED_FIVE_MAN:
            if FIVE_MAN not in self.meld_tiles:
                if meld_type == 'pon':
                    self.melds[FIVE_MAN, len(self.meld_tiles) * ONE_MELD_SIZE:
                                         len(self.meld_tiles) * ONE_MELD_SIZE
                                         + 3] = 1
                    self.discard_tile_from_hand(RED_FIVE_MAN)
                    self.discard_tile_from_hand(FIVE_MAN)
                    self.discard_tile_from_hand(FIVE_MAN)
                elif meld_type == 'kan':
                    self.melds[FIVE_MAN, len(self.meld_tiles) * ONE_MELD_SIZE:
                                         len(self.meld_tiles) * ONE_MELD_SIZE
                                         + 4] = 1
                    self.discard_tile_from_hand(RED_FIVE_MAN)
                    self.discard_tile_from_hand(FIVE_MAN)
                    self.discard_tile_from_hand(FIVE_MAN)
                    self.discard_tile_from_hand(FIVE_MAN)

                self.meld_tiles.append(FIVE_MAN)

            else:
                if meld_type == 'kan':
                    meld_index = self.meld_tiles.index(FIVE_MAN) + 1
                    self.melds[FIVE_MAN, self.meld_tiles.index(FIVE_MAN)
                               * ONE_MELD_SIZE + 3] = 1
                    self.discard_tile_from_hand(FIVE_MAN)

            self.red_dora[FIVE_MAN] = 1

        elif tile == RED_FIVE_PIN:
            if FIVE_PIN not in self.meld_tiles:
                if meld_type == 'pon':
                    self.melds[FIVE_PIN, len(self.meld_tiles) * ONE_MELD_SIZE:
                                         len(self.meld_tiles) * ONE_MELD_SIZE
                                         + 3] = 1
                    self.discard_tile_from_hand(RED_FIVE_PIN)
                    self.discard_tile_from_hand(FIVE_PIN)
                    self.discard_tile_from_hand(FIVE_PIN)
                elif meld_type == 'kan':
                    self.melds[FIVE_PIN, len(self.meld_tiles) * ONE_MELD_SIZE:
                                         len(self.meld_tiles) * ONE_MELD_SIZE
                                         + 4] = 1
                    self.discard_tile_from_hand(RED_FIVE_PIN)
                    self.discard_tile_from_hand(FIVE_PIN)
                    self.discard_tile_from_hand(FIVE_PIN)
                    self.discard_tile_from_hand(FIVE_PIN)

                self.meld_tiles.append(FIVE_PIN)

            else:
                if meld_type == 'kan':
                    meld_index = self.meld_tiles.index(FIVE_PIN) + 1
                    self.melds[FIVE_PIN, self.meld_tiles.index(FIVE_PIN)
                               * ONE_MELD_SIZE + 3] = 1
                    self.discard_tile_from_hand(FIVE_PIN)

            self.red_dora[FIVE_PIN] = 1

        elif tile == RED_FIVE_SOU:
            if FIVE_SOU not in self.meld_tiles:
                if meld_type == 'pon':
                    self.melds[FIVE_SOU, len(self.meld_tiles) * ONE_MELD_SIZE:
                                         len(self.meld_tiles) * ONE_MELD_SIZE
                                         + 3] = 1
                    self.discard_tile_from_hand(RED_FIVE_SOU)
                    self.discard_tile_from_hand(FIVE_SOU)
                    self.discard_tile_from_hand(FIVE_SOU)
                elif meld_type == 'kan':
                    self.melds[FIVE_SOU, len(self.meld_tiles) * ONE_MELD_SIZE:
                                         len(self.meld_tiles) * ONE_MELD_SIZE
                                         + 4] = 1
                    self.discard_tile_from_hand(RED_FIVE_SOU)
                    self.discard_tile_from_hand(FIVE_SOU)
                    self.discard_tile_from_hand(FIVE_SOU)
                    self.discard_tile_from_hand(FIVE_SOU)

                self.meld_tiles.append(FIVE_SOU)

            else:
                if meld_type == 'kan':
                    meld_index = self.meld_tiles.index(FIVE_SOU) + 1
                    self.melds[FIVE_SOU, self.meld_tiles.index(FIVE_SOU)
                               * ONE_MELD_SIZE + 3] = 1
                    self.discard_tile_from_hand(FIVE_SOU)

            self.red_dora[FIVE_SOU] = 1

        else:
            if tile not in self.meld_tiles:
                if meld_type == 'pon':
                    self.melds[tile, len(self.meld_tiles) * ONE_MELD_SIZE:
                                     len(self.meld_tiles) * ONE_MELD_SIZE + 3] \
                        = 1
                    self.discard_tile_from_hand(tile)
                    self.discard_tile_from_hand(tile)
                    self.discard_tile_from_hand(tile)
                elif meld_type == 'kan':
                    self.melds[tile, len(self.meld_tiles) * ONE_MELD_SIZE:
                                     len(self.meld_tiles) * ONE_MELD_SIZE + 4] \
                        = 1
                    self.discard_tile_from_hand(tile)
                    self.discard_tile_from_hand(tile)
                    self.discard_tile_from_hand(tile)
                    self.discard_tile_from_hand(tile)

                self.meld_tiles.append(tile)

            else:
                if meld_type == 'kan':
                    meld_index = self.meld_tiles.index(tile) + 1
                    self.melds[tile, self.meld_tiles.index(tile)
                               * ONE_MELD_SIZE + 3] = 1
                    self.discard_tile_from_hand(tile)

        self.melds[:, meld_index * ONE_MELD_SIZE - 5:
                      meld_index * ONE_MELD_SIZE] = \
            Agent.encode_turn_number(turn_number)

    def make_pon(self, tile, turn_number):
        self.__add_meld('pon', tile, turn_number)

        if tile == RED_FIVE_MAN:
            self.pon_tiles.append(FIVE_MAN)
        elif tile == RED_FIVE_PIN:
            self.pon_tiles.append(FIVE_PIN)
        elif tile == RED_FIVE_SOU:
            self.pon_tiles.append(FIVE_SOU)
        else:
            self.pon_tiles.append(tile)

    def make_open_kan(self, tile, turn_number):
        self.__add_meld('kan', tile, turn_number)

        if tile == RED_FIVE_MAN:
            self.open_kan.append(FIVE_MAN)
        elif tile == RED_FIVE_PIN:
            self.open_kan.append(FIVE_PIN)
        elif tile == RED_FIVE_SOU:
            self.open_kan.append(FIVE_SOU)
        else:
            self.open_kan.append(tile)

    def make_closed_kan(self, tile, turn_number):
        self.__add_meld('kan', tile, turn_number)

        if tile == RED_FIVE_MAN:
            self.closed_kan.append(FIVE_MAN)
        elif tile == RED_FIVE_PIN:
            self.closed_kan.append(FIVE_PIN)
        elif tile == RED_FIVE_SOU:
            self.closed_kan.append(FIVE_SOU)
        else:
            self.closed_kan.append(tile)

    def make_added_kan(self, tile, turn_number):
        self.__add_meld('kan', tile, turn_number)

        if tile == RED_FIVE_MAN:
            tile = FIVE_MAN
        elif tile == RED_FIVE_PIN:
            tile = FIVE_PIN
        elif tile == RED_FIVE_SOU:
            tile = FIVE_SOU

        self.pon_tiles.remove(tile)
        self.open_kan.append(tile)

    def encode_start_hand(self, start_hand):
        """
        :param start_hand: list of integer indices
        """
        self.hand = np.zeros((34, TILES_SIZE))
        self.red_dora = np.zeros((34, SELF_RED_DORA_SIZE))
        for tile in start_hand:
            self.add_tile_to_hand(tile)

    def calculate_hand(self, win_tile, hand_config, dora_indicators):
        private_tiles_array = Tiles.matrix_to_array(self.hand)

        meld_objects = []
        for pon_tile in self.pon_tiles:
            meld_objects.append(Meld(
                meld_type=Meld.PON,
                tiles=Tiles.indices_to_array([pon_tile] * 3)
            ))
        for kan_tile in self.open_kan:
            meld_objects.append(Meld(
                meld_type=Meld.KAN,
                tiles=Tiles.indices_to_array([kan_tile] * 4)
            ))
        for kan_tile in self.closed_kan:
            meld_objects.append(Meld(
                meld_type=Meld.KAN,
                tiles=Tiles.indices_to_array([kan_tile] * 4),
                is_open=False
            ))
        if self.kita_count > 0:
            kita_string = '4' * self.kita_count + 'z'
            meld_objects.append(Meld(
                meld_type=Meld.KITA, tiles=kita_string
            ))

        hand_result = HandCalculator.calculate_hand_score(
            private_tiles=private_tiles_array, win_tile=win_tile,
            melds=meld_objects, hand_config=hand_config,
            dora_indicators=dora_indicators
        )

        return hand_result

    @abstractmethod
    def eval_discard(self, target_tile, player1, player2, player3,
                     scores, round_number, honba_number, deposit_number,
                     dora_indicators):
        pass

    @abstractmethod
    def eval_pon(self, target_tile, player1, player2, player3,
                 scores, round_number, honba_number, deposit_number,
                 dora_indicators):
        pass

    @abstractmethod
    def eval_kan(self, target_tile, player1, player2, player3,
                 scores, round_number, honba_number, deposit_number,
                 dora_indicators):
        pass

    @abstractmethod
    def eval_kita(self, target_tile, player1, player2, player3,
                  scores, round_number, honba_number, deposit_number,
                  dora_indicators):
        pass

    @abstractmethod
    def eval_riichi(self, target_tile, player1, player2, player3,
                    scores, round_number, honba_number, deposit_number,
                    dora_indicators):
        pass

    @abstractmethod
    def eval_kyuushu_kyuuhai(self, target_tile, player1, player2, player3,
                             scores, round_number, honba_number, deposit_number,
                             dora_indicators):
        pass

    def eval_win(self, target_tile, player1, player2, player3,
                 scores, round_number, honba_number, deposit_number,
                 dora_indicators):
        return 1.0
