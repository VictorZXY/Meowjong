from typing import List

from hand_calculation.tile_constants import ONE_MAN, NINE_MAN, ONE_PIN, \
    NINE_PIN, ONE_SOU, NINE_SOU
from hand_calculation.tiles import Tiles
from hand_calculation.yaku import Yaku


class Ikkitsuukan(Yaku):
    """
    Hand with three consecutive shuntsu in the same suit.
    """

    def __init__(self):
        super().__init__()

    def set_attributes(self):
        self.name = 'Ikkitsuukan'
        self.english = 'Pure Straight'
        self.japanese = '一気通貫'
        self.chinese = '一气通贯'

        self.han_open = 1
        self.han_closed = 2

        self.is_yakuman = False

    def is_condition_met(self, hand: List[List[int]], *args):
        shuntsu_set = [item for item in hand if Tiles.is_shuntsu(item)]
        if len(shuntsu_set) < 3:
            return False

        man_shuntsu_set = []
        pin_shuntsu_set = []
        sou_shuntsu_set = []
        for item in shuntsu_set:
            indices = Tiles.array_to_indices(item)
            if ONE_MAN <= indices[0] <= NINE_MAN:
                man_shuntsu_set.append([i % ONE_MAN for i in indices])
            elif ONE_PIN <= Tiles.array_to_indices(item)[0] <= NINE_PIN:
                pin_shuntsu_set.append([i % ONE_PIN for i in indices])
            elif ONE_SOU <= Tiles.array_to_indices(item)[0] <= NINE_SOU:
                sou_shuntsu_set.append([i % ONE_SOU for i in indices])

        suit_sets = [man_shuntsu_set, pin_shuntsu_set, sou_shuntsu_set]
        for suit_set in suit_sets:
            if len(suit_set) >= 3:
                return [0, 1, 2] in suit_set \
                       and [3, 4, 5] in suit_set \
                       and [6, 7, 8] in suit_set

        return False
