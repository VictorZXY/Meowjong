from hand_calculation.hand_config import HandConfig
from hand_calculation.yaku import Yaku


class Chiihou(Yaku):
    """
    Winning on self-draw in the very first un-interrupted set of turns.
    Concealed kong or kita are not allowed.
    """

    def __init__(self):
        super().__init__()

    def set_attributes(self):
        self.name = 'Chiihou'
        self.english = 'Blessing of Earth'
        self.japanese = '地和'
        self.chinese = '地和'

        self.han_open = None
        self.han_closed = 13

        self.is_yakuman = True

    def is_condition_met(self, hand: HandConfig, *args):
        return hand.is_chiihou
