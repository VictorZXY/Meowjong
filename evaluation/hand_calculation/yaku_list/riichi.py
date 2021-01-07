from evaluation.hand_calculation.yaku import Yaku


class Riichi(Yaku):
    """
    Concealed waiting hand declared at 1000 points stake.
    """

    def __init__(self):
        super().__init__()

    def set_attributes(self):
        self.name = 'Riichi'
        self.english = 'Riichi'
        self.japanese = '立直'
        self.chinese = '立直'

        self.han_open = None
        self.han_closed = 1

        self.is_yakuman = False

    def is_condition_met(self, hand, *args):
        return hand.is_menzen and hand.is_riichi
