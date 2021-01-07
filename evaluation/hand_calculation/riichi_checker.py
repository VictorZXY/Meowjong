from copy import deepcopy
from itertools import product

from pyswip import Prolog

from evaluation.hand_calculation.tile_constants import ONE_MAN, NINE_MAN, \
    ONE_PIN, NINE_PIN, ONE_SOU, NINE_SOU, EAST, CHUN, YAOCHUUHAI
from evaluation.hand_calculation.tiles import Tiles


class RiichiChecker:
    @staticmethod
    def can_riichi(private_tiles, drawn_tile, closed_kan=None):
        """
        :param private_tiles: Private tiles (drawn tile excluded), represented
        by a 34-array
        :param drawn_tile: Integer index
        :param closed_kan: List of integer indices
        :return: Boolean
        """
        tiles = deepcopy(private_tiles)
        tiles[drawn_tile] += 1

        # Case of Chiitoitsu
        pair_count = 0
        triplet_count = 0
        singleton_count = 0
        for entry in tiles:
            if entry == 2:
                pair_count += 1
            elif entry == 3:
                triplet_count += 1
            elif entry == 1:
                singleton_count += 1
        counts = (pair_count, triplet_count, singleton_count)
        if counts == (7, 0, 0) or counts == (6, 0, 2) or counts == (5, 1, 1):
            return True

        # Case of Kokushi Musou
        tiles_copy = deepcopy(tiles)
        zeros_count = 0
        ones_count = 0
        twos_count = 0
        minus_ones_count = 0
        for index in YAOCHUUHAI:
            tiles_copy[index] -= 1
            if tiles_copy[index] == 0:
                zeros_count += 1
            elif tiles_copy[index] == 1:
                ones_count += 1
            elif tiles_copy[index] == 2:
                twos_count += 1
            elif tiles_copy[index] == -1:
                minus_ones_count += 1
        counts = (zeros_count, ones_count, twos_count, minus_ones_count)
        if counts == (13, 0, 0, 0) or counts == (11, 1, 0, 1) \
                or counts == (12, 1, 0, 0) or counts == (11, 0, 1, 1) \
                or counts == (10, 2, 0, 1):
            return True

        # standard case
        # manzu
        man = RiichiChecker.find_combinations(tiles, ONE_MAN, NINE_MAN)
        # pinzu
        pin = RiichiChecker.find_combinations(tiles, ONE_PIN, NINE_PIN)
        # souzu
        sou = RiichiChecker.find_combinations(tiles, ONE_SOU, NINE_SOU)
        # honours
        honours = RiichiChecker.find_combinations(tiles, EAST, CHUN)

        combinations_sets = [[]]
        if man:
            combinations_sets.append(man)
        if pin:
            combinations_sets.append(pin)
        if sou:
            combinations_sets.append(sou)
        if honours:
            combinations_sets.append(honours)
        combinations_sets.pop(0)

        for combinations in product(*combinations_sets):
            mentsu_count = 0
            pair_count = 0
            taatsu_count = 0
            singleton_count = 0

            if closed_kan:
                mentsu_count += len(closed_kan)

            for combination in list(combinations):
                for item in combination:
                    if len(item) == 3:
                        mentsu_count += 1
                    elif len(item) == 2:
                        if item[0] == item[1]:
                            pair_count += 1
                        else:
                            taatsu_count += 1
                    else:  # len(item) == 1
                        singleton_count += 1

            counts = (mentsu_count, pair_count, taatsu_count,
                      singleton_count)
            if counts == (4, 1, 0, 0) \
                    or counts == (4, 0, 1, 0) \
                    or counts == (4, 0, 0, 2) \
                    or counts == (3, 2, 0, 1) \
                    or counts == (3, 1, 1, 1):
                return True

        return False

    @staticmethod
    def find_combinations(tiles, start_index, end_index):
        """
        Find all possible combinations between the given interval in the hand
        and return their tile indices.
        :param tiles: Input tiles represented by a 34-array
        :param start_index: Start index of the interval (inclusive)
        :param end_index: End index of the interval (inclusive)
        :return: A list of lists of integer indices
        """
        indices = Tiles.array_to_indices(tiles, start_index, end_index)
        if not indices:
            return []

        combinations = []

        prolog = Prolog()
        # prolog.consult('riichi_checker.pl')
        prolog.consult('C:/Users/Victor/Desktop/To-Do List/_CST/Part II'
                       + '/Part II Project/Source Code/meowjong'
                       + '/evaluation/hand_calculation/riichi_checker.pl')
        for solution in prolog.query(
                'combination(' + str(indices) + ', Combination)'):
            combination = sorted(solution['Combination'])
            if combination not in combinations:
                combinations.append(combination)
        prolog.retractall('visited(_)')

        return combinations
