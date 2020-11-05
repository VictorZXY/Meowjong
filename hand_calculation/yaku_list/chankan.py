from hand_calculation.hand_config import HandConfig
from hand_calculation.yaku import Yaku


class Chankan(Yaku):
    """
    Winning on a tile that an opponent adds to a melded pon in order to make a
    kan.
    """

    def __init__(self):
        super().__init__()

    def set_attributes(self):
        self.name = 'Chankan'
        self.english = 'Robbing the Kan'
        self.japanese = '槍槓'
        self.chinese = '抢杠'

        self.han_open = 1
        self.han_closed = 1

        self.is_yakuman = False

    def is_condition_met(self, hand: HandConfig, *args):
        return hand.is_chankan
