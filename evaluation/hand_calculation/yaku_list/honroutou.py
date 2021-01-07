from typing import List

from evaluation.hand_calculation import YAOCHUUHAI
from evaluation.hand_calculation import Yaku


class Honroutou(Yaku):
    """
    Hand containing only terminals and honours.
    """

    def __init__(self):
        super().__init__()

    def set_attributes(self):
        self.name = 'Honroutou'
        self.english = 'All Terminals and Honours'
        self.japanese = '混老頭'
        self.chinese = '混老头'

        self.han_open = 2
        self.han_closed = 2

        self.is_yakuman = False

    def is_condition_met(self, hand: List[List[int]], *args):
        for item in hand:
            for index in range(len(item)):
                if index not in YAOCHUUHAI and item[index] != 0:
                    return False
        return True
