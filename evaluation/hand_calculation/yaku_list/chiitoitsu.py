from typing import List

from evaluation.hand_calculation.yaku import Yaku


class Chiitoitsu(Yaku):
    """
    Concealed hand with seven different pairs.
    """

    def __init__(self):
        super().__init__()

    def set_attributes(self):
        self.name = 'Chiitoitsu'
        self.english = 'Seven Pairs'
        self.japanese = '七対子'
        self.chinese = '七对子'

        self.han_open = None
        self.han_closed = 2

        self.is_yakuman = False

    def is_condition_met(self, hand: List[List[int]], *args):
        return len(hand) == 7
