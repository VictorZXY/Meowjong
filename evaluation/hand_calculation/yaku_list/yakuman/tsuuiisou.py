from typing import List

from evaluation.hand_calculation.tile_constants import HONOURS
from evaluation.hand_calculation.yaku import Yaku


class Tsuuiisou(Yaku):
    """
    Hand composed entirely of honour tiles.
    """

    def __init__(self):
        super().__init__()

    def set_attributes(self):
        self.name = 'Tsuuiisou'
        self.english = 'All Honours'
        self.japanese = '字一色'
        self.chinese = '字一色'

        self.han_open = 13
        self.han_closed = 13

        self.is_yakuman = True

    def is_condition_met(self, hand: List[List[int]], *args):
        for item in hand:
            for index in range(len(item)):
                if index not in HONOURS and item[index] != 0:
                    return False
        return True
