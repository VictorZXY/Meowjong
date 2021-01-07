from evaluation.hand_calculation.yaku import Yaku


class Tenhou(Yaku):
    """
    East winning on his initial deal. Concealed kong or kita are not allowed.
    """

    def __init__(self):
        super().__init__()

    def set_attributes(self):
        self.name = 'Tenhou'
        self.english = 'Blessing of Heaven'
        self.japanese = '天和'
        self.chinese = '天和'

        self.han_open = None
        self.han_closed = 13

        self.is_yakuman = True

    def is_condition_met(self, hand, *args):
        return hand.is_tenhou
