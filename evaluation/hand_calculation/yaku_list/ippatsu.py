from evaluation.hand_calculation import Yaku


class Ippatsu(Yaku):
    """
    An extra yaku awarded for winning within the first un-interrupted set of
    turns after declaring riichi, including the next draw by the riichi
    declarer. If the set of turns is interrupted by claims for chii, pon, kan or
    kita, including concealed kan, the chance for ippatsu is gone.
    """

    def __init__(self):
        super().__init__()

    def set_attributes(self):
        self.name = 'Ippatsu'
        self.english = 'Ippatsu'
        self.japanese = '一発'
        self.chinese = '一发'

        self.han_open = None
        self.han_closed = 1

        self.is_yakuman = False

    def is_condition_met(self, hand, *args):
        return hand.is_menzen \
               and (hand.is_riichi or hand.is_double_riichi) \
               and hand.is_ippatsu
