from typing import List

from hand_calculation.tile_constants import DRAGONS
from hand_calculation.tiles import Tiles
from hand_calculation.yaku import Yaku


class Shousangen(Yaku):
    """
    Hand with two dragon koutsu/kantsu and a pair of dragons.
    """

    def __init__(self):
        super().__init__()

    def set_attributes(self):
        self.name = 'Shousangen'
        self.english = 'Little Three Dragons'
        self.japanese = '小三元'
        self.chinese = '小三元'

        self.han_open = 2
        self.han_closed = 2

        self.is_yakuman = False

    def is_condition_met(self, hand: List[List[int]], *args):
        dragon_koutsu_count = 0
        dragon_pair_count = 0

        for item in hand:
            if Tiles.is_koutsu(item) or Tiles.is_kantsu(item):
                indices = Tiles.array_to_indices(item)
                if indices[0] in DRAGONS:
                    dragon_koutsu_count += 1
            elif Tiles.is_pair(item):
                indices = Tiles.array_to_indices(item)
                if indices[0] in DRAGONS:
                    dragon_pair_count += 1

        return dragon_koutsu_count == 2 and dragon_pair_count == 1
