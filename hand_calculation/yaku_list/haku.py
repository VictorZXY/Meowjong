from typing import List

from hand_calculation.tile_constants import HAKU
from hand_calculation.yaku import Yaku


class Haku(Yaku):
    """
    Pon/kan of haku.
    """

    def __init__(self):
        super().__init__()

    def set_attributes(self):
        self.name = 'Yakuhai: Haku'
        self.english = 'White Dragon Pon'
        self.japanese = '役牌:白'
        self.chinese = '役牌:白'

        self.han_open = 1
        self.han_closed = 1

        self.is_yakuman = False

    def is_condition_met(self, hand: List[List[int]], *args):
        return len(hand) == 5 \
               and len([item for item in hand
                        if item[HAKU] == 3 or item[HAKU] == 4]) == 1
