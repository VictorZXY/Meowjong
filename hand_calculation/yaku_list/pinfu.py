from typing import List

from hand_calculation.fu import FuCalculator
from hand_calculation.yaku import Yaku


class Pinfu(Yaku):
    """
    Concealed all shuntsu hand with a valueless pair, i.e. a concealed hand with
    four shuntsu and a pair that is neither dragons, nor seat wind, nor
    prevalent wind. The winning tile is required to finish a shuntsu with a two-
    sided wait. The hand is by definition worth no fu, only the base 30 on a
    discard, or 20 on self-draw.
    """

    def __init__(self):
        super().__init__()

    def set_attributes(self):
        self.name = 'Pinfu'
        self.english = 'Pinfu'
        self.japanese = '平和'
        self.chinese = '平和'

        self.han_open = None
        self.han_closed = 1

        self.is_yakuman = False

    def is_condition_met(self, hand: List[List[int]], win_tile, win_group,
                         hand_config, melds=None, *args):
        """
        :param hand: List of 34-arrays
        :param win_tile: Integer index
        :param win_group: 34-array
        :param hand_config: HandConfig object
        :param melds: Meld object
        :return: Boolean
        """
        fu_calculator = FuCalculator()
        fu_details = fu_calculator.calculate_fu(hand, win_tile, win_group,
                                                hand_config, melds)
        return len(hand) == 5 and len(fu_details) == 1 and (melds is None or [])
