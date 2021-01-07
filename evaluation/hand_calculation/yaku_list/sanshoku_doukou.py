from typing import List

from evaluation.hand_calculation.tile_constants import ONE_MAN, NINE_MAN, \
    ONE_PIN, NINE_PIN, ONE_SOU, NINE_SOU
from evaluation.hand_calculation.tiles import Tiles
from evaluation.hand_calculation.yaku import Yaku


class SanshokuDoukou(Yaku):
    """
    Hand with three koutsu/kantsu, one in each suit, of the same number.
    """

    def __init__(self):
        super().__init__()

    def set_attributes(self):
        self.name = 'Sanshoku Doukou'
        self.english = 'Triple Pon'
        self.japanese = '三色同刻'
        self.chinese = '三色同刻'

        self.han_open = 2
        self.han_closed = 2

        self.is_yakuman = False

    def is_condition_met(self, hand: List[List[int]], *args):
        koutsu_set = [item for item in hand
                      if Tiles.is_koutsu(item) or Tiles.is_kantsu(item)]
        if len(koutsu_set) < 3:
            return False

        man_koutsu_set = []
        pin_koutsu_set = []
        sou_koutsu_set = []
        for item in koutsu_set:
            indices = Tiles.array_to_indices(item)
            if ONE_MAN <= indices[0] <= NINE_MAN:
                man_koutsu_set.append([i for i in indices])
            elif ONE_PIN <= Tiles.array_to_indices(item)[0] <= NINE_PIN:
                pin_koutsu_set.append([i % ONE_PIN for i in indices])
            elif ONE_SOU <= Tiles.array_to_indices(item)[0] <= NINE_SOU:
                sou_koutsu_set.append([i % ONE_SOU for i in indices])

        for man_koutsu in man_koutsu_set:
            for pin_koutsu in pin_koutsu_set:
                for sou_koutsu in sou_koutsu_set:
                    if man_koutsu[0] == pin_koutsu[0] == sou_koutsu[0]:
                        return True

        return False
