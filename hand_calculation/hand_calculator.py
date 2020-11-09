from hand_calculation.agari import Agari
from hand_calculation.fu import Fu
from hand_calculation.han import Han
from hand_calculation.hand_config import HandConfig
from hand_calculation.hand_divider import HandDivider
from hand_calculation.score import Score
from hand_calculation.tile_constants import FIVE_MAN, FIVE_PIN, FIVE_SOU, \
    RED_FIVE_MAN, RED_FIVE_PIN, RED_FIVE_SOU, RED_DORA_VALUE


class NoYakuError(Exception):
    pass


class HandCalculator:
    @staticmethod
    def calculate_hand_score(private_tiles, win_tile, melds=None,
                             dora_indicators=None, hand_config=None):
        """
        Calculate hand score with explanations
        :param private_tiles: 34-array, winning tile not included
        :param win_tile: Integer index
        :param melds: List of Meld objects
        :param dora_indicators: List of integer indices
        :param hand_config: HandConfig object
        :return: A dictionary containing:
            'han_details' : A list of han details;
            'han'         : Total han (0 if hand is yakuman or above);
            'fu_details'  : A list of fu details (Empty if hand is mangan or
                            above);
            'fu'          : Total fu (0 if hand is mangan or above);
            'score'       : Total hand score;
            'yaku_level'  : Yaku level;
        """
        if not melds:
            melds = []

        if not dora_indicators:
            dora_indicators = []

        if not hand_config:
            hand_config = HandConfig()

        dora_details, dora_count = Han.count_dora(
            private_tiles=private_tiles,
            win_tile=win_tile,
            melds=melds,
            dora_indicators=dora_indicators,
            is_sanma=hand_config.is_sanma
        )

        hand_options = HandDivider.divide_hand(
            private_tiles=private_tiles,
            win_tile=win_tile,
            melds=melds
        )

        han_details = []
        han = 0
        fu_details = []
        fu = 0
        max_score = -1
        yaku_level = ''

        if isinstance(hand_options[0], int):
            han_details, han, is_yakuman = Han.calculate_han(
                hand=hand_options,
                win_tile=win_tile,
                win_group=None,
                melds=melds,
                hand_config=hand_config
            )

            if is_yakuman:
                max_score = Score.calculate_yakuman_score(
                    yakuman_list=han_details,
                    hand_config=hand_config
                )
            elif han == 5:
                max_score = Score.calculate_score(
                    han=han,
                    fu=0,
                    hand_config=hand_config
                )
            else:
                raise NoYakuError
        else:
            for hand in hand_options:
                win_group_options = HandCalculator.find_all_win_groups(
                    hand=hand,
                    win_tile=win_tile,
                    melds=melds)

                for win_group in win_group_options:
                    temp_han_details, temp_han, is_yakuman = Han.calculate_han(
                        hand=hand,
                        win_tile=win_tile,
                        win_group=win_group,
                        melds=melds,
                        hand_config=hand_config
                    )

                    if temp_han == 0:
                        continue

                    temp_fu_details, temp_fu = Fu.calculate_fu(
                        hand=hand,
                        win_tile=win_tile,
                        win_group=win_group,
                        hand_config=hand_config,
                        melds=melds
                    )

                    if is_yakuman:
                        temp_score = Score.calculate_yakuman_score(
                            yakuman_list=temp_han_details,
                            hand_config=hand_config
                        )
                    else:
                        temp_score = Score.calculate_score(
                            han=temp_han + dora_count,
                            fu=temp_fu,
                            hand_config=hand_config
                        )

                    if temp_score['score'] > max_score:
                        han_details = temp_han_details + dora_details
                        han = temp_han + dora_count
                        fu_details = temp_fu_details
                        fu = temp_fu
                        max_score = temp_score['score']
                        yaku_level = temp_score['yaku_level']

        if han == 0:
            raise NoYakuError
        else:
            return {
                'han_details': han_details,
                'han': han,
                'fu_details': fu_details,
                'fu': fu,
                'score': max_score,
                'yaku_level': yaku_level
            }

    @staticmethod
    def find_all_win_groups(hand, win_tile, melds=None):
        """
        Find all possible groups where the winning tile exists
        :param hand: List of 34-arrays
        :param win_tile: Integer index
        :param melds: List of meld objects
        :return: List of 34-arrays
        """
        if win_tile == RED_FIVE_MAN:
            win_tile = FIVE_MAN
        elif win_tile == RED_FIVE_PIN:
            win_tile = FIVE_PIN
        elif win_tile == RED_FIVE_SOU:
            win_tile = FIVE_SOU

        if not melds:
            melds = []
        else:
            melds = HandDivider.convert_melds_to_list(melds)
            for meld in melds:
                for index in [FIVE_MAN, FIVE_PIN, FIVE_SOU]:
                    if meld[index] >= RED_DORA_VALUE:
                        meld[index] = meld[index] // RED_DORA_VALUE \
                                      + meld[index] % RED_DORA_VALUE

        closed_items_set = []
        for item in hand:
            if item not in melds:
                closed_items_set.append(item)
            else:
                melds.remove(item)

        win_groups = [item for item in closed_items_set if item[win_tile] > 0]
        unique_win_groups = [list(item) for item
                             in set(tuple(item) for item in win_groups)]

        return unique_win_groups
