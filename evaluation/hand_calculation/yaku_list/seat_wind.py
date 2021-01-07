from typing import List

from evaluation.hand_calculation import EAST, SOUTH, WEST, NORTH
from evaluation.hand_calculation import Yaku


class SeatWind(Yaku):
    """
    Pon/kan of east in player's seat wind or in the prevalent wind.
    """

    def __init__(self):
        super().__init__()

    def set_attributes(self):
        self.name = 'Yakuhai: Seat Wind'
        self.english = 'Seat Wind'
        self.japanese = '役牌:門風牌'
        self.chinese = '役牌:门风牌'

        self.han_open = 1
        self.han_closed = 1

        self.is_yakuman = False

    def is_condition_met(self, hand: List[List[int]], hand_config, *args):
        if hand_config.seat_wind is None:
            return False

        if hand_config.yaku.east.is_condition_met(
                hand, hand_config.seat_wind, hand_config.prevalent_wind) \
                and hand_config.seat_wind == EAST:
            return True
        elif hand_config.yaku.south.is_condition_met(
                hand, hand_config.seat_wind, hand_config.prevalent_wind) \
                and hand_config.seat_wind == SOUTH:
            return True
        elif hand_config.yaku.west.is_condition_met(
                hand, hand_config.seat_wind, hand_config.prevalent_wind) \
                and hand_config.seat_wind == WEST:
            return True
        elif hand_config.yaku.north.is_condition_met(
                hand, hand_config.seat_wind, hand_config.prevalent_wind) \
                and hand_config.seat_wind == NORTH:
            return True
        else:
            return False
