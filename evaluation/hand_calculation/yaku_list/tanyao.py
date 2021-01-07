from typing import List

from evaluation.hand_calculation.tile_constants import YAOCHUUHAI
from evaluation.hand_calculation.yaku import Yaku


class Tanyao(Yaku):
    """
    Hand with no terminals and honours.
    """

    def __init__(self):
        super().__init__()

    def set_attributes(self):
        self.name = 'Tanyao'
        self.english = 'All Simples'
        self.japanese = '断幺九'
        self.chinese = '断幺九'

        self.han_open = 1
        self.han_closed = 1

        self.is_yakuman = False

    def is_condition_met(self, hand: List[List[int]], *args):
        for item in hand:
            for index in YAOCHUUHAI:
                if item[index] != 0:
                    return False
        return True
