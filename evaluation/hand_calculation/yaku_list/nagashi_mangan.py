from evaluation.hand_calculation.yaku import Yaku


class NagashiMangan(Yaku):
    """
    After an exhaustive draw, a player can claim this special hand if they have
    a concealed hand, have discarded only terminal and honour tiles and none of
    their discards has been claimed. The player does not have to be tenpai.
    The player receives payment equivalent to a self-drawn mangan,
    plus counters and riichi bets.
    """

    def __init__(self):
        super().__init__()

    def set_attributes(self):
        self.name = 'Nagashi Mangan'
        self.english = 'Nagashi Mangan'
        self.japanese = '流し満貫'
        self.chinese = '流局满贯'

        self.han_open = 5
        self.han_closed = 5

        self.is_yakuman = False

    def is_condition_met(self, hand, *args):
        return hand.is_nagashi_mangan
