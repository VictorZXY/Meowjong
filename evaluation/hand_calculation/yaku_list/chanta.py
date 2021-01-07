from typing import List

from evaluation.hand_calculation import TERMINALS, HONOURS
from evaluation.hand_calculation import Tiles
from evaluation.hand_calculation import Yaku


class Chanta(Yaku):
    """
    All sets contain terminals or honours, and the pair is terminals or honours.
    The hand must contain at least one honour and one shuntsu.
    """

    def __init__(self):
        super().__init__()

    def set_attributes(self):
        self.name = 'Chanta'
        self.english = 'Outside Hand'
        self.japanese = '混全帯幺九'
        self.chinese = '混全带幺九'

        self.han_open = 1
        self.han_closed = 2

        self.is_yakuman = False

    def is_condition_met(self, hand: List[List[int]], *args):
        def contains_tiles_in_indices(tiles, indices):
            for index in indices:
                if tiles[index] != 0:
                    return True
            return False

        terminal_sets_count = 0
        honour_sets_count = 0
        shuntsu_count = 0

        for item in hand:
            if Tiles.is_shuntsu(item):
                shuntsu_count += 1
            if contains_tiles_in_indices(item, TERMINALS):
                terminal_sets_count += 1
            if contains_tiles_in_indices(item, HONOURS):
                honour_sets_count += 1

        return terminal_sets_count + honour_sets_count == 5 \
               and terminal_sets_count != 0 and honour_sets_count != 0 \
               and shuntsu_count != 0
