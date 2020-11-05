from typing import List

from hand_calculation.tile_constants import WINDS
from hand_calculation.tiles import Tiles
from hand_calculation.yaku import Yaku


class Daisuushii(Yaku):
    """
    Hand with four koutsu/kantsu of winds.
    """

    def __init__(self):
        super().__init__()

    def set_attributes(self):
        self.name = 'Daisuushii'
        self.english = 'Big Four Winds'
        self.japanese = '大四喜'
        self.chinese = '大四喜'

        self.han_open = 26
        self.han_closed = 26

        self.is_yakuman = True

    def is_condition_met(self, hand: List[List[int]], *args):
        wind_koutsu_count = 0

        for item in hand:
            if Tiles.is_koutsu(item) or Tiles.is_kantsu(item):
                indices = Tiles.array_to_indices(item)
                if indices[0] in WINDS:
                    wind_koutsu_count += 1

        return wind_koutsu_count == 4
