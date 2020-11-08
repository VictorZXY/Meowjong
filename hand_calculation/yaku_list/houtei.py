
from hand_calculation.yaku import Yaku


class HouteiRaoyui(Yaku):
    """
    Winning on the discard after the last tile in the wall.
    """

    def __init__(self):
        super().__init__()

    def set_attributes(self):
        self.name = 'Houtei Raoyui'
        self.english = 'Under the River'
        self.japanese = '河底撈魚'
        self.chinese = '河底捞鱼'

        self.han_open = 1
        self.han_closed = 1

        self.is_yakuman = False

    def is_condition_met(self, hand, *args):
        return hand.is_houtei
