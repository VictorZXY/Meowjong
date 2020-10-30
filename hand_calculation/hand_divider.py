from hand_calculation.tile_constants import ONE_MAN, NINE_MAN, ONE_PIN, \
    NINE_PIN, ONE_SOU, NINE_SOU, HONOURS
from hand_calculation.tiles import Tiles
from itertools import product
from pyswip import Prolog


class HandDivider:
    def divide_hand(self, private_tiles, melds=None):
        """
        Return a list of possible divisions of a given hand, if there is no
        possible division, return the full original hand (private tiles and
        melds combined).
        :param private_tiles: Private tiles represented by a 34-array
        :param melds: Melds represented by a list of 34-arrays
        :return: A list of lists of 34-arrays
        """
        if melds is None:
            melds = []
        hands = []

        pair_indices = self.find_pairs(private_tiles)

        # case of chiitoitsu
        if len(pair_indices) == 7:
            hand = []
            for index in pair_indices:
                hand.append([2 if i == index else 0 for i in range(34)])
            hands.append(sorted(hand, reverse=True))

        # find all possible standard, 4 mentsu + 1 pair division
        for pair_index in pair_indices:
            private_tiles_copy = private_tiles[:]
            private_tiles_copy[pair_index] -= 2

            # manzu mentsu
            man = self.find_mentsu_combinations(private_tiles_copy, ONE_MAN,
                                                NINE_MAN)
            # pinzu mentsu
            pin = self.find_mentsu_combinations(private_tiles_copy, ONE_PIN,
                                                NINE_PIN)
            # souzu mentsu
            sou = self.find_mentsu_combinations(private_tiles_copy, ONE_SOU,
                                                NINE_SOU)
            # honours (koutsu only)
            honours = []
            for index in HONOURS:
                if private_tiles_copy[index] == 3:
                    honours.append([index] * 3)
            if honours:
                honours = [honours]

            combination_sets = [[[pair_index] * 2]]
            if man:
                combination_sets.append(man)
            if pin:
                combination_sets.append(pin)
            if sou:
                combination_sets.append(sou)
            if honours:
                combination_sets.append(honours)
            for meld in melds:
                meld_indices = Tiles.array_to_indices(meld)
                combination_sets.append([meld_indices])

            for combination in product(*combination_sets):
                hand_indices = []
                for item in list(combination):
                    if isinstance(item[0], list):
                        for x in item:
                            hand_indices.append(x)
                    else:
                        hand_indices.append(item)

                if len(hand_indices) == 5:
                    hand_array = []
                    for item in hand_indices:
                        hand_array.append(Tiles.indices_to_array(item))
                    hand_array = sorted(hand_array, reverse=True)
                    if hand_array not in hands:
                        hands.append(hand_array)

        if hands:
            return sorted(hands, reverse=True)
        else:
            full_hand = private_tiles[:]
            for meld in melds:
                full_hand = [x + y for x, y in zip(full_hand, meld)]
            return full_hand

    @staticmethod
    def find_pairs(tiles):
        """
        Find all possible pairs in the hand return their tile indices.
        :param tiles: Input tiles represented by a 34-array
        :return: A list of tile indices
        """
        pair_indices = []

        for index in range(len(tiles)):
            # ignore koutsu and kantsu of honour tiles, as it cannot be a pair
            if index in HONOURS and tiles[index] != 2:
                continue
            elif tiles[index] >= 2:
                pair_indices.append(index)

        return pair_indices

    @staticmethod
    def find_mentsu_combinations(tiles, start_index, end_index):
        """
        Find all possible mentsu combinations between the given interval in the
        hand and return their tile indices.
        :param tiles: Input tiles represented by a 34-array
        :param start_index: Start index of the interval (inclusive)
        :param end_index: End index of the interval (inclusive)
        :return: A list of lists of mentsu indicies
        """
        indices = Tiles.array_to_indices(tiles, start_index, end_index)

        if not indices:
            return []
        elif len(indices) % 3 != 0:
            return []

        combinations = []

        prolog = Prolog()
        # prolog.consult("hand_divider.pl")
        prolog.consult("C:/Users/Victor/Desktop/To-Do List/_CST/Part II"
                       + "/Part II Project/Source Code/meowjong"
                       + "/hand_calculation/hand_divider.pl")
        for solution in prolog.query(
                "mentsu_combination(" + str(indices) + ", Combination)"):
            combination = sorted(solution["Combination"])
            if combination not in combinations:
                combinations.append(combination)
        prolog.retractall("traversed(_)")

        return combinations
