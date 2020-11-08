from hand_calculation.meld import Meld
from hand_calculation.tile_constants import ONE_MAN, FIVE_MAN, NINE_MAN, \
    ONE_PIN, FIVE_PIN, NINE_PIN, ONE_SOU, FIVE_SOU, NINE_SOU, EAST, NORTH, \
    HAKU, CHUN, RED_FIVE_MAN, RED_FIVE_PIN, RED_FIVE_SOU, TERMINALS, DRAGONS, \
    YAOCHUUHAI, RED_DORA_VALUE
from hand_calculation.tiles import Tiles


class HanCalculator:
    DORA = 'Dora from dora indicators'
    RED_DORA = 'Red dora'
    NUKI_DORA = 'Nuki-dora'

    @staticmethod
    def count_dora(private_tiles, win_tile, melds=None, dora_indicators=None,
                   is_sanma=False):
        """
        Count number of dora in hand
        :param private_tiles: List of 34-arrays
        :param win_tile: Integer index
        :param melds: Meld object
        :param dora_indicators: List of integer indices
        :param is_sanma: Boolean
        :return: A list of dora details, and an integer representing total
        number of dora
        """
        if not melds:
            melds = []

        if not dora_indicators:
            dora_indicators = []

        dora_details = []

        # count nuki-dora
        nuki_dora_count = sum([Tiles.tiles_count(meld) for meld in melds
                               if meld.type == Meld.KITA])
        if nuki_dora_count > 0:
            dora_details.append({'han': nuki_dora_count,
                                 'reason': HanCalculator.NUKI_DORA})

        # count red dora
        red_dora_count = 0

        for index in [FIVE_MAN, FIVE_PIN, FIVE_SOU]:
            if private_tiles[index] >= RED_DORA_VALUE:
                red_dora_count += private_tiles[index] // RED_DORA_VALUE

        if win_tile == RED_FIVE_MAN or win_tile == RED_FIVE_PIN \
                or win_tile == RED_FIVE_SOU:
            red_dora_count += 1

        for meld in melds:
            for index in [FIVE_MAN, FIVE_PIN, FIVE_SOU]:
                if meld[index] >= RED_DORA_VALUE:
                    red_dora_count += meld[index] // RED_DORA_VALUE

        if red_dora_count > 0:
            dora_details.append({'han': red_dora_count,
                                 'reason': HanCalculator.RED_DORA})

        # count dora from dora indicators
        dora_list = []

        for indicator in dora_indicators:
            # 4-player mahjong and 3-player mahjong differ in manzu
            if is_sanma:
                # manzu
                if indicator == ONE_MAN:
                    dora_list.append(NINE_MAN)
                elif indicator == NINE_MAN:
                    dora_list.append(ONE_MAN)
                # pinzu
                elif ONE_PIN <= indicator < NINE_PIN:
                    dora_list.append(indicator + 1)
                elif indicator == NINE_PIN:
                    dora_list.append(ONE_PIN)
                # souzu
                elif ONE_SOU <= indicator < NINE_SOU:
                    dora_list.append(indicator + 1)
                elif indicator == NINE_SOU:
                    dora_list.append(ONE_PIN)
                # winds
                elif EAST <= indicator < NORTH:
                    dora_list.append(indicator + 1)
                elif indicator == NORTH:
                    dora_list.append(EAST)
                # dragons
                elif HAKU <= indicator < CHUN:
                    dora_list.append(indicator + 1)
                elif indicator == CHUN:
                    dora_list.append(HAKU)
                else:  # if ONE_MAN < indicator < NINE_MAN:
                    assert False, '2-8m does not exist in Sanma'
            else:
                if indicator == NINE_MAN:
                    dora_list.append(ONE_MAN)
                elif indicator == NINE_PIN:
                    dora_list.append(ONE_PIN)
                elif indicator == NINE_SOU:
                    dora_list.append(ONE_PIN)
                elif indicator == NORTH:
                    dora_list.append(EAST)
                elif indicator == CHUN:
                    dora_list.append(HAKU)
                else:
                    dora_list.append(indicator + 1)

        dora_count = 0

        for index in dora_list:
            if index in [FIVE_MAN, FIVE_PIN, FIVE_SOU]:
                dora_count += private_tiles[index] // RED_DORA_VALUE \
                              + private_tiles[index] % RED_DORA_VALUE
            else:
                dora_count += private_tiles[index]

        if win_tile in dora_list:
            dora_count += 1

        for meld in melds:
            for index in dora_list:
                if index in [FIVE_MAN, FIVE_PIN, FIVE_SOU]:
                    dora_count += meld.tiles[index] // RED_DORA_VALUE \
                                  + meld.tiles[index] % RED_DORA_VALUE
                else:
                    dora_count += meld.tiles[index]

        if dora_count > 0:
            dora_details.append({'han': dora_count,
                                 'reason': HanCalculator.DORA})

        return dora_details, dora_count + red_dora_count + nuki_dora_count

    @staticmethod
    def calculate_han(hand, win_tile, melds=None, hand_config=None):
        """
        Calculate hand han with explanations (dora not counted)
        :param hand: List of 34-arrays
        :param win_tile: Integer index
        :param melds: Meld object
        :param hand_config: HandConfig object
        :return: A list of han details, and an integer representing total
        number of han
        """
        if win_tile == RED_FIVE_MAN:
            win_tile = FIVE_MAN
        elif win_tile == RED_FIVE_PIN:
            win_tile = FIVE_PIN
        elif win_tile == RED_FIVE_SOU:
            win_tile = FIVE_SOU

        if not melds:
            melds = []
