from evaluation.hand_calculation.yaku import Yaku


class DoubleRiichi(Yaku):
    """
    An extra yaku awarded for declaring riichi in the first set of turns of the
    hand, i.e. in the player's very first turn. The first set of turns must be
    uninterrupted, i.e. if any claims for chii, pon, kan or kita, including
    concealed kan, has occurred before the riichi declaration, double riichi is
    not possible.
    """

    def __init__(self):
        super().__init__()

    def set_attributes(self):
        self.name = 'Double Riichi'
        self.english = 'Double Riichi'
        self.japanese = '両立直'
        self.chinese = '两立直'

        self.han_open = None
        self.han_closed = 2

        self.is_yakuman = False

    def is_condition_met(self, hand, *args):
        return hand.is_menzen and hand.is_double_riichi
