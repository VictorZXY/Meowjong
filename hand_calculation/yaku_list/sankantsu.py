from typing import List

from hand_calculation.meld import Meld
from hand_calculation.yaku import Yaku


class Sankantsu(Yaku):
    """
    Hand with three kantsu.
    """

    def __init__(self):
        super().__init__()

    def set_attributes(self):
        self.name = 'Sankantsu'
        self.english = 'Three Kan'
        self.japanese = '三槓子'
        self.chinese = '三杠子'

        self.han_open = 2
        self.han_closed = 2

        self.is_yakuman = False

    def is_condition_met(self, hand: List[List[int]], melds=None, *args):
        kantsu_set = [item for item in melds if item.type == Meld.KAN]
        return len(kantsu_set) == 3
