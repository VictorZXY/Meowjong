from copy import deepcopy

import numpy as np

from data_processing.data_preprocessing_constants import TILES_SIZE, \
    SELF_RED_DORA_SIZE, MELDS_SIZE, KITA_SIZE, DISCARDS_SIZE, TENHOU_TILE_INDEX, \
    ONE_MELD_SIZE, TURN_NUMBER_SIZE
from hand_calculation.riichi_checker import RiichiChecker
from hand_calculation.tenpai import Tenpai
from hand_calculation.tile_constants import FIVE_MAN, FIVE_PIN, FIVE_SOU, \
    NORTH, RED_FIVE_MAN, RED_FIVE_PIN, RED_FIVE_SOU


class Player:
    def __init__(self):
        self.hand = np.zeros((34, TILES_SIZE))
        self.red_dora = np.zeros((34, SELF_RED_DORA_SIZE))
        self.melds = np.zeros((34, MELDS_SIZE))
        self.kita = np.zeros((34, KITA_SIZE))
        self.discards = np.zeros((34, DISCARDS_SIZE))
        self.log_draws = None
        self.log_discards = None
        self.meld_tiles = []
        self.closed_kan = []
        self.riichi_status = False
        self.riichi_turn_number = 0

    @staticmethod
    def __encode_number(number, size):
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

        return np.sum(self.hand[tile], dtype=np.int32) == 3 \
               or 4 in self.hand.sum(axis=1)

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

    def add_kita(self):
        index = 0
        while self.kita[NORTH, index] != 0:
            index += 1
        self.kita[NORTH, index] = 1
        self.discard_tile_from_hand(44)

    def add_meld(self, type, tile, turn_number):
        """
        :param type: String, 'pon' or 'kan'
        :param tile: Tenhou-encoded integer index of a tile
        :param turn_number: Integer
        """
        if TENHOU_TILE_INDEX[tile] == RED_FIVE_MAN:
            if FIVE_MAN not in self.meld_tiles:
                if type == 'pon':
                    self.melds[FIVE_MAN, len(self.meld_tiles) * ONE_MELD_SIZE:
                                         len(self.meld_tiles) * ONE_MELD_SIZE
                                         + 3] = 1
                    self.discard_tile_from_hand(51)
                    self.discard_tile_from_hand(15)
                    self.discard_tile_from_hand(15)
                elif type == 'kan':
                    self.melds[FIVE_MAN, len(self.meld_tiles) * ONE_MELD_SIZE:
                                         len(self.meld_tiles) * ONE_MELD_SIZE
                                         + 4] = 1
                    self.discard_tile_from_hand(51)
                    self.discard_tile_from_hand(15)
                    self.discard_tile_from_hand(15)
                    self.discard_tile_from_hand(15)

                self.meld_tiles.append(FIVE_MAN)

            else:
                if type == 'kan':
                    self.melds[FIVE_MAN, self.meld_tiles.index(FIVE_MAN)
                               * ONE_MELD_SIZE + 3] = 1
                    self.discard_tile_from_hand(51)

            self.red_dora[FIVE_MAN] = 1

        elif TENHOU_TILE_INDEX[tile] == RED_FIVE_PIN:
            if FIVE_PIN not in self.meld_tiles:
                if type == 'pon':
                    self.melds[FIVE_PIN, len(self.meld_tiles) * ONE_MELD_SIZE:
                                         len(self.meld_tiles) * ONE_MELD_SIZE
                                         + 3] = 1
                    self.discard_tile_from_hand(52)
                    self.discard_tile_from_hand(25)
                    self.discard_tile_from_hand(25)
                elif type == 'kan':
                    self.melds[FIVE_PIN, len(self.meld_tiles) * ONE_MELD_SIZE:
                                         len(self.meld_tiles) * ONE_MELD_SIZE
                                         + 4] = 1
                    self.discard_tile_from_hand(52)
                    self.discard_tile_from_hand(25)
                    self.discard_tile_from_hand(25)
                    self.discard_tile_from_hand(25)

                self.meld_tiles.append(FIVE_PIN)

            else:
                if type == 'kan':
                    self.melds[FIVE_PIN, self.meld_tiles.index(FIVE_PIN)
                               * ONE_MELD_SIZE + 3] = 1
                    self.discard_tile_from_hand(52)

            self.red_dora[FIVE_PIN] = 1

        elif TENHOU_TILE_INDEX[tile] == RED_FIVE_SOU:
            if FIVE_SOU not in self.meld_tiles:
                if type == 'pon':
                    self.melds[FIVE_SOU, len(self.meld_tiles) * ONE_MELD_SIZE:
                                         len(self.meld_tiles) * ONE_MELD_SIZE
                                         + 3] = 1
                    self.discard_tile_from_hand(53)
                    self.discard_tile_from_hand(35)
                    self.discard_tile_from_hand(35)
                elif type == 'kan':
                    self.melds[FIVE_SOU, len(self.meld_tiles) * ONE_MELD_SIZE:
                                         len(self.meld_tiles) * ONE_MELD_SIZE
                                         + 4] = 1
                    self.discard_tile_from_hand(53)
                    self.discard_tile_from_hand(35)
                    self.discard_tile_from_hand(35)
                    self.discard_tile_from_hand(35)

                self.meld_tiles.append(FIVE_SOU)

            else:
                if type == 'kan':
                    self.melds[FIVE_SOU, self.meld_tiles.index(FIVE_SOU)
                               * ONE_MELD_SIZE + 3] = 1
                    self.discard_tile_from_hand(53)

            self.red_dora[FIVE_SOU] = 1

        else:
            converted_tile = TENHOU_TILE_INDEX[tile]
            if converted_tile not in self.meld_tiles:
                if type == 'pon':
                    self.melds[converted_tile, len(self.meld_tiles)
                                               * ONE_MELD_SIZE:
                                               len(self.meld_tiles)
                                               * ONE_MELD_SIZE + 3] = 1
                    self.discard_tile_from_hand(tile)
                    self.discard_tile_from_hand(tile)
                    self.discard_tile_from_hand(tile)
                elif type == 'kan':
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
                if type == 'kan':
                    self.melds[converted_tile,
                               self.meld_tiles.index(converted_tile)
                               * ONE_MELD_SIZE + 3] = 1
                    self.discard_tile_from_hand(tile)

        self.melds[:, len(self.meld_tiles) * ONE_MELD_SIZE - 5:
                      len(self.meld_tiles) * ONE_MELD_SIZE] = \
            Player.__encode_turn_number(turn_number)

    def encode_start_hand(self, start_hand):
        """
        :param start_hand: list of Tenhou-encoded integer indices
        :param player: Player object
        :return: hand: (34, 4) np.array; red_dora: (34, 1) np.array
        """
        self.hand = np.zeros((34, TILES_SIZE))
        self.red_dora = np.zeros((34, SELF_RED_DORA_SIZE))
        for tile in start_hand:
            self.add_tile_to_hand(tile)
