from math import prod
from typing import List

from evaluation.hand_calculation.tiles import Tiles
from evaluation.hand_calculation.tile_constants import YAOCHUUHAI
from evaluation.hand_calculation.yaku import Yaku


class KokushiMusou13Men(Yaku):
    """
    Concealed hand with one of each of the 13 different terminal and honour
    tiles plus one extra terminal or honour tile, waiting for all 13 different
    terminal and honour tiles.
    """

    def __init__(self):
        super().__init__()

    def set_attributes(self):
        self.name = 'Kokushi Musou 13-Men Machi'
        self.english = 'Thirteen Orphans 13-Way Wait'
        self.japanese = '国士無双１３面待ち'
        self.chinese = '国士无双十三面'

        self.han_open = None
        self.han_closed = 26

        self.is_yakuman = True

    def is_condition_met(self, hand: List[int], win_tile, *args):
        """
        :param hand: List of 34-arrays
        :param win_tile: Integer index
        :return: Boolean
        """
        if Tiles.tiles_count(hand) == 14:
            hand[win_tile] -= 1
            return prod([hand[i] for i in YAOCHUUHAI]) == 1
        else:
            return False
