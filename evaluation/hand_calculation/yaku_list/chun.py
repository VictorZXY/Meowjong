from typing import List

from evaluation.hand_calculation import CHUN
from evaluation.hand_calculation import Yaku


class Chun(Yaku):
    """
    Pon/kan of chun.
    """

    def __init__(self):
        super().__init__()

    def set_attributes(self):
        self.name = 'Yakuhai: Chun'
        self.english = 'Red Dragon Pon'
        self.japanese = '役牌:中'
        self.chinese = '役牌:中'

        self.han_open = 1
        self.han_closed = 1

        self.is_yakuman = False

    def is_condition_met(self, hand: List[List[int]], *args):
        return len(hand) == 5 \
               and len([item for item in hand
                        if item[CHUN] == 3 or item[CHUN] == 4]) == 1
