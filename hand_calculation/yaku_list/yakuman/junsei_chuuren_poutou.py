from functools import reduce
from typing import List


from hand_calculation.tile_constants import NINE_MAN, ONE_PIN, ONE_SOU, \
    RED_FIVE_MAN, RED_FIVE_PIN, RED_FIVE_SOU, MANZU, PINZU, SOUZU, HONOURS
from hand_calculation.tiles import Tiles
from hand_calculation.yaku import Yaku


class JunseiChuurenPoutou(Yaku):
    """
    Concealed hand consisting of the tiles 1112345678999 in the same suit,
    waiting for any one extra tile in the same suit.
    """

    def __init__(self):
        super().__init__()

    def set_attributes(self):
        self.name = 'Junsei Chuuren Poutou'
        self.english = 'Pure Nine Gates'
        self.japanese = '純正九蓮宝燈'
        self.chinese = '纯正九莲宝灯'

        self.han_open = None
        self.han_closed = 26

        self.is_yakuman = True

    def is_condition_met(self, hand: List[List[int]], win_tile, hand_config,
                         *args):
        """
        :param hand: List of 34-arrays
        :param win_tile: Integer index
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
            mod_base = NINE_MAN + 1
        elif pin_sets_count != 0:
            mod_base = ONE_PIN
        else:  # if sou_sets_count != 0:
            mod_base = ONE_SOU

        hand_indices = [Tiles.array_to_indices(item) for item in hand]
        indices = reduce(lambda x, y: x + y, hand_indices)
        indices = [i % mod_base for i in indices]

        # 1112345678999 in private tiles
        if win_tile == RED_FIVE_MAN or win_tile == RED_FIVE_PIN \
                or win_tile == RED_FIVE_SOU:
            indices.remove(4)
        else:
            indices.remove(win_tile % mod_base)

        return sorted(indices) == [0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 8, 8]
