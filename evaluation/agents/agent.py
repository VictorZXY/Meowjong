from itertools import product
from abc import ABC, abstractmethod

import numpy as np

from data_processing.data_preprocessing_constants import TILES_SIZE, \
    SELF_RED_DORA_SIZE, MELDS_SIZE, KITA_SIZE, DISCARDS_SIZE
from evaluation.hand_calculation.han import Han
from evaluation.hand_calculation.hand_calculator import HandCalculator
from evaluation.hand_calculation.hand_config import HandConfig
from evaluation.hand_calculation.hand_divider import HandDivider
from evaluation.hand_calculation.meld import Meld
from evaluation.hand_calculation.riichi_checker import RiichiChecker
from evaluation.hand_calculation.tile_constants import ONE_MAN, FIVE_MAN, \
    NINE_MAN, ONE_PIN, FIVE_PIN, NINE_PIN, ONE_SOU, FIVE_SOU, NINE_SOU, EAST, \
    NORTH, CHUN, RED_FIVE_MAN, RED_FIVE_PIN, RED_FIVE_SOU, YAOCHUUHAI
from evaluation.hand_calculation.tiles import Tiles


class Agent(ABC):
    def __init__(self):
        self.hand = np.zeros((34, TILES_SIZE))
        self.red_dora = np.zeros((34, SELF_RED_DORA_SIZE))
        self.melds = np.zeros((34, MELDS_SIZE))
        self.kita = np.zeros((34, KITA_SIZE))
        self.discards = np.zeros((34, DISCARDS_SIZE))
        self.log_draws = None
        self.log_discards = None
        self.meld_tiles = []
        self.pon_tiles = []
        self.open_kan = []
        self.closed_kan = []
        self.riichi_status = False
        self.riichi_turn_number = 0
        self.naki_status = False

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
        :return: Boolean
        """
        if kan_count == 4 or remaining_tiles == 0:
            return False

        if target_tile == RED_FIVE_MAN:
            target_tile = FIVE_MAN
        elif target_tile == RED_FIVE_PIN:
            target_tile = FIVE_PIN
        elif target_tile == RED_FIVE_SOU:
            target_tile = FIVE_SOU

        if np.sum(self.hand[target_tile], dtype=np.int32) == 3 \
                or 4 in self.hand.sum(axis=1):
            if not self.riichi_status:
                return True
            else:
                tiles = Tiles.matrices_to_array(self.hand)
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
                            return True

                return False
        else:
            return False

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

        for meld in self.meld_tiles:
            if meld == target_tile or self.hand[meld, 0] == 1:
                return True
        return False

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
        if self.riichi_status:
            return False
        if self.meld_tiles:
            return False

        if target_tile == RED_FIVE_MAN:
            target_tile = FIVE_MAN
        elif target_tile == RED_FIVE_PIN:
            target_tile = FIVE_PIN
        elif target_tile == RED_FIVE_SOU:
            target_tile = FIVE_SOU

        private_tiles_array = Tiles.matrices_to_array(self.hand)

        return RiichiChecker.can_riichi(private_tiles_array, target_tile,
                                        self.closed_kan)

    def has_kyuushu_kyuuhai(self, target_tile, player1, player2, player3=None):
        yaochuuhai_count = np.sum(self.hand[YAOCHUUHAI, 0], dtype=np.int32)
        if target_tile in YAOCHUUHAI:
            yaochuuhai_count += 1

        if player3 is not None:
            return yaochuuhai_count >= 9 and \
                   not (self.naki_status or player1.naki_status
                        or player2.naki_status or player3.naki_status)
        else:
            return yaochuuhai_count >= 9 and \
                   not (self.naki_status or player1.naki_status
                        or player2.naki_status)

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

        private_tiles_array = Tiles.matrices_to_array(self.hand)
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

                    if han > 0 or is_yakuman:
                        return True

            return False

    @abstractmethod
    def eval_discard(self, target_tile):
        pass

    @abstractmethod
    def eval_pon(self, target_tile):
        pass

    @abstractmethod
    def eval_kan(self, target_tile):
        pass

    @abstractmethod
    def eval_kita(self, target_tile):
        pass

    @abstractmethod
    def eval_riichi(self, target_tile):
        pass

    @abstractmethod
    def eval_kyuushu_kyuuhai(self, target_tile):
        pass

    @abstractmethod
    def eval_win(self, target_tile):
        pass
