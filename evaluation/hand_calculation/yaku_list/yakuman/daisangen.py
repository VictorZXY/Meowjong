from typing import List

from evaluation.hand_calculation.tile_constants import DRAGONS
from evaluation.hand_calculation.tiles import Tiles
from evaluation.hand_calculation.yaku import Yaku


class Daisangen(Yaku):
    """
    Hand with three koutsu/kantsu of dragons.
    """

    def __init__(self):
        super().__init__()

    def set_attributes(self):
        self.name = 'Daisangen'
        self.english = 'Big Three Dragons'
        self.japanese = '大三元'
        self.chinese = '大三元'

        self.han_open = 13
        self.han_closed = 13

        self.is_yakuman = True

    def is_condition_met(self, hand: List[List[int]], *args):
        dragon_koutsu_count = 0

        for item in hand:
            if Tiles.is_koutsu(item) or Tiles.is_kantsu(item):
                indices = Tiles.array_to_indices(item)
                if indices[0] in DRAGONS:
                    dragon_koutsu_count += 1

        return dragon_koutsu_count == 3
