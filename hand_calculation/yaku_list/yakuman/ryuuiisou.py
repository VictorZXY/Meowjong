from typing import List

from hand_calculation.tile_constants import GREEN_TILES
from hand_calculation.yaku import Yaku


class Ryuuiisou(Yaku):
    """
    Hand composed entirely of green tiles.
    """

    def __init__(self):
        super().__init__()

    def set_attributes(self):
        self.name = 'Ryuuiisou'
        self.english = 'All Green'
        self.japanese = '緑一色'
        self.chinese = '绿一色'

        self.han_open = 13
        self.han_closed = 13

        self.is_yakuman = True

    def is_condition_met(self, hand: List[List[int]], *args):
        for item in hand:
            for index in range(len(item)):
                if index not in GREEN_TILES and item[index] != 0:
                    return False
        return True
