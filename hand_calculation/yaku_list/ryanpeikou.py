from typing import List

from hand_calculation.tiles import Tiles
from hand_calculation.yaku import Yaku


class Ryanpeikou(Yaku):
    """
    Concealed hand with four shuntsu which two and two form Iipeikou.
    No additional fan for Iipeikou is counted.
    """

    def __init__(self):
        super().__init__()

    def set_attributes(self):
        self.name = 'Ryanpeikou'
        self.english = 'Twice Pure Double Chii'
        self.japanese = '二盃口'
        self.chinese = '二杯口'

        self.han_open = None
        self.han_closed = 3

        self.is_yakuman = False

    def is_condition_met(self, hand: List[List[int]], *args):
        shuntsu_set = [item for item in hand if Tiles.is_shuntsu(item)]

        identical_shuntsu_counts = []
        for x in shuntsu_set:
            count = 0
            for y in shuntsu_set:
                if x == y:
                    count += 1
            if count >= 2:
                identical_shuntsu_counts.append(count)

        return len(identical_shuntsu_counts) == 4
