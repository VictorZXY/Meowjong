from typing import List

from evaluation.hand_calculation.tiles import Tiles
from evaluation.hand_calculation.yaku import Yaku


class Iipeikou(Yaku):
    """
    Concealed hand with two completely identical shuntsu, i.e. the same values
    in the same suit.
    """

    def __init__(self):
        super().__init__()

    def set_attributes(self):
        self.name = 'Iipeikou'
        self.english = 'Pure Double Chii'
        self.japanese = '一盃口'
        self.chinese = '一杯口'

        self.han_open = None
        self.han_closed = 1

        self.is_yakuman = False

    def is_condition_met(self, hand: List[List[int]], hand_config, *args):
        if not hand_config.is_menzen:
            return False

        shuntsu_set = [item for item in hand if Tiles.is_shuntsu(item)]

        identical_shuntsu_count = 0
        for x in shuntsu_set:
            count = 0
            for y in shuntsu_set:
                if x == y:
                    count += 1
            if count > identical_shuntsu_count:
                identical_shuntsu_count = count

        return identical_shuntsu_count >= 2
