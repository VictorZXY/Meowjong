from math import prod
from typing import List

from hand_calculation.tile_constants import YAOCHUUHAI
from hand_calculation.tiles import Tiles
from hand_calculation.yaku import Yaku


class KokushiMusou(Yaku):
    """
    Concealed hand with one of each of the 13 different terminal and honour
    tiles plus one extra terminal or honour tile.
    """

    def __init__(self):
        super().__init__()

    def set_attributes(self):
        self.name = 'Kokushi Musou'
        self.english = 'Thirteen Orphans'
        self.japanese = '国士無双'
        self.chinese = '国士无双'

        self.han_open = None
        self.han_closed = 13

        self.is_yakuman = True

    def is_condition_met(self, hand: List[int], *args):
        if Tiles.tiles_count(hand) == 14 \
                and prod([hand[i] for i in YAOCHUUHAI]) == 2:
            return True
        else:
            return False
