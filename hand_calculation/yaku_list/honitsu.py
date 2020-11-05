from typing import List

from hand_calculation.tile_constants import MANZU, PINZU, SOUZU, HONOURS
from hand_calculation.tiles import Tiles
from hand_calculation.yaku import Yaku


class Honitsu(Yaku):
    """
    Hand with tiles from only one of the three suits, in combination with
    honours.
    """

    def __init__(self):
        super().__init__()

    def set_attributes(self):
        self.name = 'Honitsu'
        self.english = 'Half Flush'
        self.japanese = '混一色'
        self.chinese = '混一色'

        self.han_open = 2
        self.han_closed = 3

        self.is_yakuman = False

    def is_condition_met(self, hand: List[List[int]], *args):
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

        return contains_only_one_suit and honour_sets_count != 0
