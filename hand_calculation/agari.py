from hand_calculation.hand_divider import HandDivider
from hand_calculation.yaku_list.yakuman import KokushiMusou


class Agari:
    @staticmethod
    def is_agari(private_tiles, melds=None):
        """
        Determine whether a given hand is complete. Yaku are not counted.
        :param private_tiles: Private tiles (winning tile included) represented
        by a 34-array
        :param melds: Melds represented by a list of Meld objects
        :return: Boolean
        """
        hand_divider = HandDivider()
        divisions = hand_divider.divide_hand(private_tiles, melds)

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
