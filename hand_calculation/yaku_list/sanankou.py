from typing import List


from hand_calculation.tile_constants import FIVE_MAN, FIVE_PIN, FIVE_SOU, \
    RED_FIVE_MAN, RED_FIVE_PIN, RED_FIVE_SOU
from hand_calculation.tiles import Tiles
from hand_calculation.yaku import Yaku


class Sanankou(Yaku):
    """
    Hand with three concealed koutsu/kantsu. Note, the entire hand is not
    required to be concealed.
    """

    def __init__(self):
        super().__init__()

    def set_attributes(self):
        self.name = 'Sanankou'
        self.english = 'Three Concealed Pon'
        self.japanese = '三暗刻'
        self.chinese = '三暗刻'

        self.han_open = 2
        self.han_closed = 2

        self.is_yakuman = False

    def is_condition_met(self, hand: List[List[int]], win_tile,
                         hand_config, melds=None, *args):
        """
        :param hand: List of 34-arrays
        :param win_tile: Integer index
        :param hand_config: HandConfig object
        :param melds: List of Meld objects
        :return: Boolean
        """

        def win_tile_in_item(tiles, win_tile):
            if win_tile == RED_FIVE_MAN:
                return tiles[FIVE_MAN] >= 4
            elif win_tile == RED_FIVE_PIN:
                return tiles[FIVE_PIN] >= 4
            elif win_tile == RED_FIVE_SOU:
                return tiles[FIVE_SOU] >= 4
            elif win_tile == FIVE_MAN or win_tile == FIVE_PIN \
                    or win_tile == FIVE_SOU:
                return tiles[win_tile] != 0 and tiles[win_tile] != 4
            else:
                return tiles[win_tile] != 0

        open_meld_set = [item.tiles for item in melds if item.is_open]
        shuntsu_set = [item for item in hand
                       if Tiles.is_shuntsu(item)
                       and win_tile_in_item(item, win_tile)
                       and item not in open_meld_set]
        koutsu_set = [item for item in hand
                      if Tiles.is_koutsu(item) or Tiles.is_kantsu(item)]

        closed_koutsu_set = []
        for item in koutsu_set:
            if item not in open_meld_set:
                if win_tile_in_item(item, win_tile) \
                        and not hand_config.is_tsumo and not shuntsu_set:
                    continue
                closed_koutsu_set.append(item)

        return len(closed_koutsu_set) == 3
