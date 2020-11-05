from typing import List

from hand_calculation.tile_constants import EAST
from hand_calculation.yaku import Yaku


class East(Yaku):
    """
    Pon/kan of east in player's seat wind or in the prevalent wind.
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

    def is_condition_met(self, hand: List[List[int]], player_wind, round_wind,
                         *args):
        if len(hand) == 5 \
                and len([item for item in hand
                         if item[player_wind] == 3
                            or item[player_wind] == 4]) == 1 \
                and player_wind == EAST:
            return True
        elif len(hand) == 5 \
                and len([item for item in hand if
                         item[round_wind] == 3 or item[round_wind] == 4]) == 1 \
                and round_wind == EAST:
            return True
        else:
            return False
