from copy import deepcopy
from itertools import product

from pyswip import Prolog

from evaluation.hand_calculation.meld import Meld
from evaluation.hand_calculation.tile_constants import ONE_MAN, FIVE_MAN, \
    NINE_MAN, ONE_PIN, FIVE_PIN, NINE_PIN, ONE_SOU, FIVE_SOU, NINE_SOU, \
    RED_FIVE_MAN, RED_FIVE_PIN, RED_FIVE_SOU, HONOURS, RED_DORA_VALUE
from evaluation.hand_calculation.tiles import Tiles


class HandDivider:
    @staticmethod
    def divide_hand(private_tiles, win_tile=None, melds=None):
        """
        Return a list of possible divisions of a given hand, if there is no
        possible division, return the full original hand (private tiles and
        melds combined).
        :param private_tiles: Private tiles (winning tile may be included or
        not), represented by a 34-array
        :param win_tile: Integer index, only specified when it is not included
        in private_tiles
        :param melds: Melds represented by a list of Meld objects
        :return: A list of lists of 34-arrays
        """
        tiles = deepcopy(private_tiles)
        if win_tile is not None:
            if win_tile == RED_FIVE_MAN:
                tiles[FIVE_MAN] += RED_DORA_VALUE
            elif win_tile == RED_FIVE_PIN:
                tiles[FIVE_PIN] += RED_DORA_VALUE
            elif win_tile == RED_FIVE_SOU:
                tiles[FIVE_SOU] += RED_DORA_VALUE
            else:
                tiles[win_tile] += 1
        for index in [FIVE_MAN, FIVE_PIN, FIVE_SOU]:
            if tiles[index] >= RED_DORA_VALUE:
                tiles[index] = tiles[index] // RED_DORA_VALUE \
                               + tiles[index] % RED_DORA_VALUE

        if melds is None:
            melds_copy = []
        else:
            melds_copy = HandDivider.convert_melds_to_list(melds)
            for meld in melds_copy:
                for index in [FIVE_MAN, FIVE_PIN, FIVE_SOU]:
                    if meld[index] >= RED_DORA_VALUE:
                        meld[index] = meld[index] // RED_DORA_VALUE \
                                      + meld[index] % RED_DORA_VALUE

        divisions = []

        pair_indices = HandDivider.find_pairs(tiles)

        # case of chiitoitsu
        if len(pair_indices) == 7:
            division = []
            for index in pair_indices:
                division.append([2 if i == index else 0 for i in range(34)])
            divisions.append(sorted(division, reverse=True))

        # find all possible standard, 4 mentsu + 1 pair division
        for pair_index in pair_indices:
            tiles_copy = deepcopy(tiles)
            tiles_copy[pair_index] -= 2

            # manzu mentsu
            man = HandDivider.find_mentsu_combinations(
                tiles_copy, ONE_MAN, NINE_MAN)
            # pinzu mentsu
            pin = HandDivider.find_mentsu_combinations(
                tiles_copy, ONE_PIN, NINE_PIN)
            # souzu mentsu
            sou = HandDivider.find_mentsu_combinations(
                tiles_copy, ONE_SOU, NINE_SOU)
            # honours (koutsu only)
            honours = []
            for index in HONOURS:
                if tiles_copy[index] == 3:
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
            for meld in melds_copy:
                meld_indices = Tiles.array_to_indices(meld)
                combination_sets.append([meld_indices])

            for combination in product(*combination_sets):
                division_indices = []
                for item in list(combination):
                    if isinstance(item[0], list):
                        for x in item:
                            division_indices.append(x)
                    else:
                        division_indices.append(item)

                if len(division_indices) == 5:
                    division_array = []
                    for item in division_indices:
                        division_array.append(Tiles.indices_to_array(item))
                    division_array = sorted(division_array, reverse=True)
                    if division_array not in divisions:
                        divisions.append(division_array)

        if divisions:
            return sorted(divisions, reverse=True)
        else:
            full_hand = deepcopy(tiles)
            for meld in melds_copy:
                full_hand = [x + y for x, y in zip(full_hand, meld)]
            return full_hand

    @staticmethod
    def convert_melds_to_list(melds):
        melds_list = []
        for meld in melds:
            # exclude kita from hand division
            if meld.type != Meld.KITA:
                melds_list.append(deepcopy(meld.tiles))
        return melds_list

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
        :return: A list of lists of mentsu indices
        """
        indices = Tiles.array_to_indices(tiles, start_index, end_index)

        if not indices:
            return []
        elif len(indices) % 3 != 0:
            return []

        combinations = []

        prolog = Prolog()
        # prolog.consult('hand_divider.pl')
        prolog.consult('C:/Users/Victor/Desktop/To-Do List/_CST/Part II'
                       + '/Part II Project/Source Code/meowjong'
                       + '/evaluation/hand_calculation/hand_divider.pl')
        for solution in prolog.query(
                'mentsu_combination(' + str(indices) + ', Combination)'):
            combination = sorted(solution['Combination'])
            if combination not in combinations:
                combinations.append(combination)
        prolog.retractall('traversed(_)')

        return combinations
