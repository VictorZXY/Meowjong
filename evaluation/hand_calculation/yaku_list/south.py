from typing import List

from evaluation.hand_calculation.tile_constants import SOUTH
from evaluation.hand_calculation.yaku import Yaku


class South(Yaku):
    """
    Pon/kan of south in player's seat wind or in the prevalent wind.
    """

    def __init__(self):
        super().__init__()

    def set_attributes(self):
        self.name = 'Yakuhai: Seat/Prevalent Wind'
        self.english = 'Seat/Prevalent Wind'
        self.japanese = '役牌:門風牌/場風牌'
        self.chinese = '役牌:门风牌/场风牌'

        self.han_open = 1
        self.han_closed = 1

        self.is_yakuman = False

    def is_condition_met(self, hand: List[List[int]], seat_wind, prevalent_wind,
                         *args):
        if len(hand) == 5 and seat_wind is not None:
            if len([item for item in hand
                    if item[seat_wind] == 3 or item[seat_wind] == 4]) == 1 \
                    and seat_wind == SOUTH:
                return True

        if len(hand) == 5 and prevalent_wind is not None:
            if len([item for item in hand
                    if item[prevalent_wind] == 3
                       or item[prevalent_wind] == 4]) == 1 \
                    and prevalent_wind == SOUTH:
                return True

        return False
