from functools import reduce
from typing import List

from hand_calculation.hand_config import HandConfig
from hand_calculation.tile_constants import ONE_MAN, ONE_PIN, ONE_SOU, MANZU, \
    PINZU, SOUZU, HONOURS
from hand_calculation.tiles import Tiles
from hand_calculation.yaku import Yaku


class ChuurenPoutou(Yaku):
    """
    Concealed hand consisting of the tiles 1112345678999 in the same suit plus
    any one extra tile in the same suit.
    """

    def __init__(self):
        super().__init__()

    def set_attributes(self):
        self.name = 'Chuuren Poutou'
        self.english = 'Nine Gates'
        self.japanese = '九蓮宝燈'
        self.chinese = '九莲宝灯'

        self.han_open = None
        self.han_closed = 13

        self.is_yakuman = True

    def is_condition_met(self, hand: List[List[int]], hand_config: HandConfig,
                         *args):
        """
        :param hand: List of 34-arrays
        :param hand_config: HandConfig object
        :return: Boolean
        """
        if not hand_config.is_menzen:
            return False

        honour_sets_count = 0
        man_sets_count = 0
        pin_sets_count = 0
        sou_sets_count = 0

        for item in hand:
            indices = Tiles.array_to_indices(item)

            if indices[0] in HONOURS:
                honour_sets_count += 1

            if indices[0] in MANZU:
                man_sets_count += 1
            elif indices[0] in PINZU:
                pin_sets_count += 1
            elif indices[0] in SOUZU:
                sou_sets_count += 1

        suit_sets_counts = [man_sets_count, pin_sets_count, sou_sets_count]
        contains_only_one_suit = len([count for count in suit_sets_counts
                                      if count != 0]) == 1

        if not (contains_only_one_suit and honour_sets_count == 0):
            return False

        if man_sets_count != 0:
            mod_base = ONE_MAN
        elif pin_sets_count != 0:
            mod_base = ONE_PIN
        else:  # if sou_sets_count != 0:
            mod_base = ONE_SOU

        hand_indices = [Tiles.array_to_indices(item) for item in hand]
        indices = reduce(lambda x, y: x + y, hand_indices)
        indices = [i % mod_base for i in indices]

        # 111
        if len([i for i in indices if i == 0]) < 3:
            return False

        # 999
        if len([i for i in indices if i == 8]) < 3:
            return False

        # 123456789 and one extra tile in any of them
        indices.remove(0)
        indices.remove(0)
        indices.remove(8)
        indices.remove(8)
        return reduce(lambda x, y: x * y, indices) == 2
