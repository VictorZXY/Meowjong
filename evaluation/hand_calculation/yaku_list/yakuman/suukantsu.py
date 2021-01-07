from typing import List

from evaluation.hand_calculation import Meld
from evaluation.hand_calculation import Yaku


class Suukantsu(Yaku):
    """
    Hand with four kantsu.
    """

    def __init__(self):
        super().__init__()

    def set_attributes(self):
        self.name = 'Suukantsu'
        self.english = 'Four Kan'
        self.japanese = '四槓子'
        self.chinese = '四杠子'

        self.han_open = 13
        self.han_closed = 13

        self.is_yakuman = True

    def is_condition_met(self, hand: List[List[int]], melds=None, *args):
        kantsu_set = [item for item in melds if item.type == Meld.KAN]
        return len(kantsu_set) == 4
