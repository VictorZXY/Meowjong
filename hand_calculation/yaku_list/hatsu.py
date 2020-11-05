from typing import List

from hand_calculation.tile_constants import HATSU
from hand_calculation.yaku import Yaku


class Hatsu(Yaku):
    """
    Pon/kan of hatsu.
    """

    def __init__(self):
        super().__init__()

    def set_attributes(self):
        self.name = 'Yakuhai: Hatsu'
        self.english = 'Green Dragon Pon'
        self.japanese = '役牌:發'
        self.chinese = '役牌:发'

        self.han_open = 1
        self.han_closed = 1

        self.is_yakuman = False

    def is_condition_met(self, hand: List[List[int]], *args):
        return len(hand) == 5 \
               and len([item for item in hand
                        if item[HATSU] == 3 or item[HATSU] == 4]) == 1
