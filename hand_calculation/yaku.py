class Yaku:
    name = None
    english = None
    japanese = None
    chinese = None
    han_open = None
    han_closed = None
    is_yakuman = None

    def __init__(self):
        self.set_attributes()

    def __str__(self):
        return self.name

    def __repr__(self):
        # for calls in array
        return self.__str__()

    def is_condition_met(self, hand, *args) -> bool:
        """
        Check whether this yaku exists in the given hand, with the specified
        division.
        :param hand: The hand (winning tile included) represented by a list of
                     34-arrays (a single 34-array in the case of kokushi musou)
        :param args: Some yaku may require additional attributes
        :return: Boolean
        """
        raise NotImplementedError

    def set_attributes(self):
        """
        Set name and han values related to the yaku.
        """
        raise NotImplementedError
