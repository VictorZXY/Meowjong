from typing import List

from hand_calculation.tile_constants import TERMINALS
from hand_calculation.yaku import Yaku


class Chinroutou(Yaku):
    """
    Hand composed entirely of terminal tiles.
    """

    def __init__(self):
        super().__init__()

    def set_attributes(self):
        self.name = 'Chinroutou'
        self.english = 'All Terminals'
        self.japanese = '清老頭'
        self.chinese = '清老头'

        self.han_open = 13
        self.han_closed = 13

        self.is_yakuman = True

    def is_condition_met(self, hand: List[List[int]], *args):
        for item in hand:
            for index in range(len(item)):
                if index not in TERMINALS and item[index] != 0:
                    return False
        return True
