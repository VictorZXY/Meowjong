from typing import List

from evaluation.hand_calculation import Tiles
from evaluation.hand_calculation import WINDS
from evaluation.hand_calculation import Yaku


class Shousuushii(Yaku):
    """
    Hand with three koutsu/kantsu of winds and a pair of winds.
    """

    def __init__(self):
        super().__init__()

    def set_attributes(self):
        self.name = 'Shousuushii'
        self.english = 'Little Four Winds'
        self.japanese = '小四喜'
        self.chinese = '小四喜'

        self.han_open = 13
        self.han_closed = 13

        self.is_yakuman = True

    def is_condition_met(self, hand: List[List[int]], *args):
        wind_koutsu_count = 0
        wind_pair_count = 0

        for item in hand:
            if Tiles.is_koutsu(item) or Tiles.is_kantsu(item):
                indices = Tiles.array_to_indices(item)
                if indices[0] in WINDS:
                    wind_koutsu_count += 1
            elif Tiles.is_pair(item):
                indices = Tiles.array_to_indices(item)
                if indices[0] in WINDS:
                    wind_pair_count += 1

        return wind_koutsu_count == 3 and wind_pair_count == 1
