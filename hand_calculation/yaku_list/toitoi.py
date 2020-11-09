from typing import List

from hand_calculation.tiles import Tiles
from hand_calculation.yaku import Yaku


class Toitoihou(Yaku):
    """
    Hand with four koutsu/kantsu and a pair.
    """

    def __init__(self):
        super().__init__()

    def set_attributes(self):
        self.name = 'Toitoihou'
        self.english = 'All Pon'
        self.japanese = '対々和'
        self.chinese = '对对和'

        self.han_open = 2
        self.han_closed = 2

        self.is_yakuman = False

    def is_condition_met(self, hand: List[List[int]], *args):
        koutsu_set = [item for item in hand \
                      if Tiles.is_koutsu(item) or Tiles.is_kantsu(item)]
        return len(koutsu_set) == 4
