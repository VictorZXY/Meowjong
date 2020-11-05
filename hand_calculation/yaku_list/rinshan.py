from hand_calculation.hand_config import HandConfig
from hand_calculation.yaku import Yaku


class RinshanKaihou(Yaku):
    """
    Winning on a replacement tile after declaring a kan or kita.
    """

    def __init__(self):
        super().__init__()

    def set_attributes(self):
        self.name = 'Rinshan Kaihou'
        self.english = 'After a Kan/Kita'
        self.japanese = '嶺上開花'
        self.chinese = '岭上开花'

        self.han_open = 1
        self.han_closed = 1

        self.is_yakuman = False

    def is_condition_met(self, hand: HandConfig, *args):
        return hand.is_rinshan
