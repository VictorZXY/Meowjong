from typing import List

from hand_calculation.tile_constants import TERMINALS
from hand_calculation.tiles import Tiles
from hand_calculation.yaku import Yaku


class Junchan(Yaku):
    """
    All sets contain terminals, and the pair is terminals.
    The hand must contain at least one shuntsu.
    """

    def __init__(self):
        super().__init__()

    def set_attributes(self):
        self.name = 'Junchan'
        self.english = 'Terminals in All Sets'
        self.japanese = '純全帯幺九'
        self.chinese = '纯全带幺九'

        self.han_open = 2
        self.han_closed = 3

        self.is_yakuman = False

    def is_condition_met(self, hand: List[List[int]], *args):
        def contains_tiles_in_indices(tiles, indices):
            for index in indices:
                if tiles[index] != 0:
                    return True
            return False

        terminal_sets_count = 0
        shuntsu_count = 0

        for item in hand:
            if Tiles.is_shuntsu(item):
                shuntsu_count += 1
            if contains_tiles_in_indices(item, TERMINALS):
                terminal_sets_count += 1

        return terminal_sets_count == 5 and shuntsu_count != 0
