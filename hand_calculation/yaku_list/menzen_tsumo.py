from hand_calculation.hand_config import HandConfig
from hand_calculation.yaku import Yaku


class MenzenTsumo(Yaku):
    """
    Winning on a self-draw on a concealed hand.
    """

    def __init__(self):
        super().__init__()

    def set_attributes(self):
        self.name = 'Menzen Tsumo'
        self.english = 'Fully Concealed Hand'
        self.japanese = '門前清自摸和'
        self.chinese = '门前清自摸和'

        self.han_open = None
        self.han_closed = 1

        self.is_yakuman = False

    def is_condition_met(self, hand: HandConfig, *args):
        return hand.is_menzen_tsumo
