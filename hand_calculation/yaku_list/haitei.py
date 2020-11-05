from hand_calculation.hand_config import HandConfig
from hand_calculation.yaku import Yaku


class HaiteiRaoyue(Yaku):
    """
    Winning on self-draw on the last tile in the wall.
    """

    def __init__(self):
        super().__init__()

    def set_attributes(self):
        self.name = 'Haitei Raoyue'
        self.english = 'Under the Sea'
        self.japanese = '海底撈月'
        self.chinese = '海底捞月'

        self.han_open = 1
        self.han_closed = 1

        self.is_yakuman = False

    def is_condition_met(self, hand: HandConfig, *args):
        return hand.is_haitei
