from itertools import product

import numpy as np

from data_processing.data_processing_constants import TILES_SIZE, \
    SELF_RED_DORA_SIZE, MELDS_SIZE, KITA_SIZE, DISCARDS_SIZE, \
    TENHOU_TILE_INDEX, ONE_MELD_SIZE, TURN_NUMBER_SIZE
from evaluation.hand_calculation.tile_constants import ONE_MAN, FIVE_MAN, \
    NINE_MAN, ONE_PIN, FIVE_PIN, NINE_PIN, ONE_SOU, FIVE_SOU, NINE_SOU, EAST, \
    NORTH, CHUN, RED_FIVE_MAN, RED_FIVE_PIN, RED_FIVE_SOU

from evaluation.hand_calculation.riichi_checker import RiichiChecker
from evaluation.hand_calculation.tiles import Tiles


class Player:
    def __init__(self):
        self.hand = np.zeros((34, TILES_SIZE))
        self.red_dora = np.zeros((34, SELF_RED_DORA_SIZE))
        self.melds = np.zeros((34, MELDS_SIZE))
        self.kita = np.zeros((34, KITA_SIZE))
        self.kita_index = 0
        self.discards = np.zeros((34, DISCARDS_SIZE))
        self.discard_index = 0
        self.log_draws = None
        self.log_discards = None
        self.meld_tiles = []
        self.closed_kan = []
        self.riichi_status = False
        self.riichi_turn_number = 0

    @staticmethod
    def __encode_number(number, size):
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
    def __encode_turn_number(turn_number):
        """
        :param turn_number: integer
        :return: (34, 5) np.array
        """
        return Player.__encode_number(turn_number, TURN_NUMBER_SIZE)

    def encode_riichi_status(self):
        if self.riichi_status:
            riichi_status_encoded = np.ones((34, 1))
        else:
            riichi_status_encoded = np.zeros((34, 1))

        return np.concatenate((
            riichi_status_encoded,
            Player.__encode_turn_number(self.riichi_turn_number)
        ), axis=1)

    def can_pon(self, target_tile):
        """
        :param target_tile: Tenhou-encoded integer index of a tile
        :return: Boolean
        """
        if self.riichi_status:
            return False

        tile = TENHOU_TILE_INDEX[target_tile]
        if tile == RED_FIVE_MAN:
            tile = FIVE_MAN
        elif tile == RED_FIVE_PIN:
            tile = FIVE_PIN
        elif tile == RED_FIVE_SOU:
            tile = FIVE_SOU

        return np.sum(self.hand[tile], dtype=np.int32) >= 2

    def can_closed_kan(self, target_tile):
        """
        :param target_tile: Tenhou-encoded integer index of a tile
        :return: Boolean
        """
        tile = TENHOU_TILE_INDEX[target_tile]
        if tile == RED_FIVE_MAN:
            tile = FIVE_MAN
        elif tile == RED_FIVE_PIN:
            tile = FIVE_PIN
        elif tile == RED_FIVE_SOU:
            tile = FIVE_SOU

        if np.sum(self.hand[tile], dtype=np.int32) == 3 \
                or 4 in self.hand.sum(axis=1):
            if not self.riichi_status:
                return True
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
                                if item[0] == item[1] == item[2] == tile:
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
                            return True

                return False
        else:
            return False

    def can_open_kan(self, target_tile):
        """
        :param target_tile: Tenhou-encoded integer index of a tile
        :return: Boolean
        """
        tile = TENHOU_TILE_INDEX[target_tile]
        if tile == RED_FIVE_MAN:
            tile = FIVE_MAN
        elif tile == RED_FIVE_PIN:
            tile = FIVE_PIN
        elif tile == RED_FIVE_SOU:
            tile = FIVE_SOU

        return np.sum(self.hand[tile], dtype=np.int32) == 3

    def can_add_kan(self, target_tile):
        """
        :param target_tile: Tenhou-encoded integer index of a tile
        :return: Boolean
        """
        if self.riichi_status:
            return False

        tile = TENHOU_TILE_INDEX[target_tile]
        if tile == RED_FIVE_MAN:
            tile = FIVE_MAN
        elif tile == RED_FIVE_PIN:
            tile = FIVE_PIN
        elif tile == RED_FIVE_SOU:
            tile = FIVE_SOU

        for meld in self.meld_tiles:
            if meld == tile or self.hand[meld, 0] == 1:
                return True
        return False

    def can_kita(self, target_tile):
        """
        :param target_tile: Tenhou-encoded integer index of a tile
        :return: Boolean
        """
        if self.riichi_status:
            return target_tile == 44
        else:
            return target_tile == 44 \
                   or np.sum(self.hand[NORTH], dtype=np.int32) > 0

    def can_riichi(self, target_tile):
        """
        :param target_tile: Tenhou-encoded integer index of a tile
        :return: Boolean
        """
        if self.riichi_status:
            return False
        if self.meld_tiles:
            if sorted(self.meld_tiles) != sorted(self.closed_kan):
                return False

        tile = TENHOU_TILE_INDEX[target_tile]
        if tile == RED_FIVE_MAN:
            tile = FIVE_MAN
        elif tile == RED_FIVE_PIN:
            tile = FIVE_PIN
        elif tile == RED_FIVE_SOU:
            tile = FIVE_SOU

        private_tiles_array = np.sum(self.hand, axis=1, dtype=np.int32).tolist()

        return RiichiChecker.can_riichi(private_tiles_array, tile,
                                        self.closed_kan)

    def add_tile_to_hand(self, tile):
        """
        :param tile: Tenhou-encoded integer index of a tile
        """
        if TENHOU_TILE_INDEX[tile] == RED_FIVE_MAN:
            index = 0
            while self.hand[FIVE_MAN, index] != 0:
                index += 1
            self.hand[FIVE_MAN, index] = 1
            self.red_dora[FIVE_MAN] = 1
        elif TENHOU_TILE_INDEX[tile] == RED_FIVE_PIN:
            index = 0
            while self.hand[FIVE_PIN, index] != 0:
                index += 1
            self.hand[FIVE_PIN, index] = 1
            self.red_dora[FIVE_PIN] = 1
        elif TENHOU_TILE_INDEX[tile] == RED_FIVE_SOU:
            index = 0
            while self.hand[FIVE_SOU, index] != 0:
                index += 1
            self.hand[FIVE_SOU, index] = 1
            self.red_dora[FIVE_SOU] = 1
        else:
            converted_tile = TENHOU_TILE_INDEX[tile]
            index = 0
            while self.hand[converted_tile, index] != 0:
                index += 1
            self.hand[converted_tile, index] = 1

    def discard_tile_from_hand(self, tile):
        """
        :param tile: Tenhou-encoded integer index of a tile
        """
        if TENHOU_TILE_INDEX[tile] == RED_FIVE_MAN:
            index = 0
            while index < 4 and self.hand[FIVE_MAN, index] != 0:
                index += 1
            self.hand[FIVE_MAN, index - 1] = 0
            self.red_dora[FIVE_MAN] = 0
        elif TENHOU_TILE_INDEX[tile] == RED_FIVE_PIN:
            index = 0
            while index < 4 and self.hand[FIVE_PIN, index] != 0:
                index += 1
            self.hand[FIVE_PIN, index - 1] = 0
            self.red_dora[FIVE_PIN] = 0
        elif TENHOU_TILE_INDEX[tile] == RED_FIVE_SOU:
            index = 0
            while index < 4 and self.hand[FIVE_SOU, index] != 0:
                index += 1
            self.hand[FIVE_SOU, index - 1] = 0
            self.red_dora[FIVE_SOU] = 0
        else:
            converted_tile = TENHOU_TILE_INDEX[tile]
            index = 0
            while index < 4 and self.hand[converted_tile, index] != 0:
                index += 1
            self.hand[converted_tile, index - 1] = 0

    def add_discard(self, tile):
        """
        :param tile: Tenhou-encoded integer index of a tile
        """
        converted_tile = TENHOU_TILE_INDEX[tile]
        if converted_tile == RED_FIVE_MAN:
            converted_tile = FIVE_MAN
        elif converted_tile == RED_FIVE_PIN:
            converted_tile = FIVE_PIN
        elif converted_tile == RED_FIVE_SOU:
            converted_tile = FIVE_SOU

        self.discards[converted_tile, self.discard_index] = 1
        self.discard_index += 1
        self.discard_tile_from_hand(tile)

    def add_kita(self):
        self.kita[NORTH, self.kita_index] = 1
        self.kita_index += 1
        self.discard_tile_from_hand(44)  # 44 is Tenhou-encoded index for North

    def add_meld(self, meld_type, tile, turn_number):
        """
        :param meld_type: String, 'pon' or 'kan'
        :param tile: Tenhou-encoded integer index of a tile
        :param turn_number: Integer
        """
        meld_index = len(self.meld_tiles) + 1
        if TENHOU_TILE_INDEX[tile] == RED_FIVE_MAN:
            if FIVE_MAN not in self.meld_tiles:
                if meld_type == 'pon':
                    self.melds[FIVE_MAN, len(self.meld_tiles) * ONE_MELD_SIZE:
                                         len(self.meld_tiles) * ONE_MELD_SIZE
                                         + 3] = 1
                    self.discard_tile_from_hand(51)
                    self.discard_tile_from_hand(15)
                    self.discard_tile_from_hand(15)
                elif meld_type == 'kan':
                    self.melds[FIVE_MAN, len(self.meld_tiles) * ONE_MELD_SIZE:
                                         len(self.meld_tiles) * ONE_MELD_SIZE
                                         + 4] = 1
                    self.discard_tile_from_hand(51)
                    self.discard_tile_from_hand(15)
                    self.discard_tile_from_hand(15)
                    self.discard_tile_from_hand(15)

                self.meld_tiles.append(FIVE_MAN)

            else:
                if meld_type == 'kan':
                    meld_index = self.meld_tiles.index(FIVE_MAN) + 1
                    self.melds[FIVE_MAN, self.meld_tiles.index(FIVE_MAN)
                               * ONE_MELD_SIZE + 3] = 1
                    self.discard_tile_from_hand(51)

            self.red_dora[FIVE_MAN] = 1

        elif TENHOU_TILE_INDEX[tile] == RED_FIVE_PIN:
            if FIVE_PIN not in self.meld_tiles:
                if meld_type == 'pon':
                    self.melds[FIVE_PIN, len(self.meld_tiles) * ONE_MELD_SIZE:
                                         len(self.meld_tiles) * ONE_MELD_SIZE
                                         + 3] = 1
                    self.discard_tile_from_hand(52)
                    self.discard_tile_from_hand(25)
                    self.discard_tile_from_hand(25)
                elif meld_type == 'kan':
                    self.melds[FIVE_PIN, len(self.meld_tiles) * ONE_MELD_SIZE:
                                         len(self.meld_tiles) * ONE_MELD_SIZE
                                         + 4] = 1
                    self.discard_tile_from_hand(52)
                    self.discard_tile_from_hand(25)
                    self.discard_tile_from_hand(25)
                    self.discard_tile_from_hand(25)

                self.meld_tiles.append(FIVE_PIN)

            else:
                if meld_type == 'kan':
                    meld_index = self.meld_tiles.index(FIVE_PIN) + 1
                    self.melds[FIVE_PIN, self.meld_tiles.index(FIVE_PIN)
                               * ONE_MELD_SIZE + 3] = 1
                    self.discard_tile_from_hand(52)

            self.red_dora[FIVE_PIN] = 1

        elif TENHOU_TILE_INDEX[tile] == RED_FIVE_SOU:
            if FIVE_SOU not in self.meld_tiles:
                if meld_type == 'pon':
                    self.melds[FIVE_SOU, len(self.meld_tiles) * ONE_MELD_SIZE:
                                         len(self.meld_tiles) * ONE_MELD_SIZE
                                         + 3] = 1
                    self.discard_tile_from_hand(53)
                    self.discard_tile_from_hand(35)
                    self.discard_tile_from_hand(35)
                elif meld_type == 'kan':
                    self.melds[FIVE_SOU, len(self.meld_tiles) * ONE_MELD_SIZE:
                                         len(self.meld_tiles) * ONE_MELD_SIZE
                                         + 4] = 1
                    self.discard_tile_from_hand(53)
                    self.discard_tile_from_hand(35)
                    self.discard_tile_from_hand(35)
                    self.discard_tile_from_hand(35)

                self.meld_tiles.append(FIVE_SOU)

            else:
                if meld_type == 'kan':
                    meld_index = self.meld_tiles.index(FIVE_SOU) + 1
                    self.melds[FIVE_SOU, self.meld_tiles.index(FIVE_SOU)
                               * ONE_MELD_SIZE + 3] = 1
                    self.discard_tile_from_hand(53)

            self.red_dora[FIVE_SOU] = 1

        else:
            converted_tile = TENHOU_TILE_INDEX[tile]
            if converted_tile not in self.meld_tiles:
                if meld_type == 'pon':
                    self.melds[converted_tile, len(self.meld_tiles)
                                               * ONE_MELD_SIZE:
                                               len(self.meld_tiles)
                                               * ONE_MELD_SIZE + 3] = 1
                    self.discard_tile_from_hand(tile)
                    self.discard_tile_from_hand(tile)
                    self.discard_tile_from_hand(tile)
                elif meld_type == 'kan':
                    self.melds[converted_tile, len(self.meld_tiles)
                                               * ONE_MELD_SIZE:
                                               len(self.meld_tiles)
                                               * ONE_MELD_SIZE + 4] = 1
                    self.discard_tile_from_hand(tile)
                    self.discard_tile_from_hand(tile)
                    self.discard_tile_from_hand(tile)
                    self.discard_tile_from_hand(tile)

                self.meld_tiles.append(converted_tile)

            else:
                if meld_type == 'kan':
                    meld_index = self.meld_tiles.index(converted_tile) + 1
                    self.melds[converted_tile,
                               self.meld_tiles.index(converted_tile)
                               * ONE_MELD_SIZE + 3] = 1
                    self.discard_tile_from_hand(tile)

        self.melds[:, meld_index * ONE_MELD_SIZE - 5:
                      meld_index * ONE_MELD_SIZE] = \
            Player.__encode_turn_number(turn_number)

    def encode_start_hand(self, start_hand):
        """
        :param start_hand: list of Tenhou-encoded integer indices
        :return: hand: (34, 4) np.array; red_dora: (34, 1) np.array
        """
        self.hand = np.zeros((34, TILES_SIZE))
        self.red_dora = np.zeros((34, SELF_RED_DORA_SIZE))
        for tile in start_hand:
            self.add_tile_to_hand(tile)
