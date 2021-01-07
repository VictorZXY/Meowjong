from evaluation.hand_calculation.agari import Agari


class Tenpai:
    @staticmethod
    def calculate_tenpai(private_tiles, melds=None):
        """
        Calculate whether a given hand is ready, and return the winning tiles
        needed if it is a ready hand.
        :param private_tiles: Private tiles, represented by a 34-array
        :param melds: Melds represented by a list of Meld objects
        :return: List of integer indices
        """
        result = []
        for index in range(35):
            if Agari.is_agari(private_tiles, win_tile=index, melds=melds):
                result.append(index)
        return result
