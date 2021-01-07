from evaluation.hand_calculation import HandDivider
from evaluation.hand_calculation.yaku_list.yakuman import KokushiMusou


class Agari:
    @staticmethod
    def is_agari(private_tiles, win_tile=None, melds=None):
        """
        Determine whether a given hand is complete. Yaku are not counted.
        :param private_tiles: Private tiles (winning tile may be included or
        not), represented by a 34-array
        :param win_tile: Integer index, only specified when it is not included
        in private_tiles
        :param melds: Melds represented by a list of Meld objects
        :return: Boolean
        """
        divisions = HandDivider.divide_hand(
            private_tiles, win_tile=win_tile, melds=melds)

        # case of kokushi musou
        if isinstance(divisions[0], int):
            kokushi_musou = KokushiMusou()
            if kokushi_musou.is_condition_met(divisions):
                return True
            else:
                return False
        else:
            # as long as divisions is a list of lists and is not empty, there is
            # at least a valid division, which means the hand is complete
            return True
