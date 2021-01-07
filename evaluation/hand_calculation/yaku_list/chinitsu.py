from typing import List

from evaluation.hand_calculation import MANZU, PINZU, SOUZU, HONOURS
from evaluation.hand_calculation import Tiles
from evaluation.hand_calculation import Yaku


class Chinitsu(Yaku):
    """
    Hand composed entirely of tiles from only one of the three suits.
    No honours allowed.
    """

    def __init__(self):
        super().__init__()

    def set_attributes(self):
        self.name = 'Chinitsu'
        self.english = 'Full Flush'
        self.japanese = '清一色'
        self.chinese = '清一色'

        self.han_open = 5
        self.han_closed = 6

        self.is_yakuman = False

    def is_condition_met(self, hand: List[List[int]], *args):
        honour_sets_count = 0
        man_sets_count = 0
        pin_sets_count = 0
        sou_sets_count = 0

        for item in hand:
            indices = Tiles.array_to_indices(item)

            if indices[0] in HONOURS:
                honour_sets_count += 1

            if indices[0] in MANZU:
                man_sets_count += 1
            elif indices[0] in PINZU:
                pin_sets_count += 1
            elif indices[0] in SOUZU:
                sou_sets_count += 1

        suit_sets_counts = [man_sets_count, pin_sets_count, sou_sets_count]
        contains_only_one_suit = len([count for count in suit_sets_counts
                                      if count != 0]) == 1

        return contains_only_one_suit and honour_sets_count == 0
