from evaluation.hand_calculation.meld import Meld
from evaluation.hand_calculation.tile_constants import ONE_MAN, FIVE_MAN, \
    SIX_MAN, NINE_MAN, ONE_PIN, FIVE_PIN, SIX_PIN, NINE_PIN, ONE_SOU, \
    FIVE_SOU, SIX_SOU, NINE_SOU, EAST, NORTH, HAKU, CHUN, RED_FIVE_MAN, \
    RED_FIVE_PIN, RED_FIVE_SOU, RED_DORA_VALUE
from evaluation.hand_calculation.tiles import Tiles


class IllegalKitaError(Exception):
    pass


class Han:
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
        :param melds: List of Meld objects
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
        nuki_dora_count = sum([Tiles.tiles_count(meld.tiles) for meld in melds
                               if meld.type == Meld.KITA])
        if nuki_dora_count > 0:
            if is_sanma:
                dora_details.append({'han': nuki_dora_count,
                                     'reason': Han.NUKI_DORA})
            else:
                raise IllegalKitaError

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
                if meld.tiles[index] >= RED_DORA_VALUE:
                    red_dora_count += meld.tiles[index] // RED_DORA_VALUE

        if red_dora_count > 0:
            dora_details.append({'han': red_dora_count, 'reason': Han.RED_DORA})

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
                elif indicator == RED_FIVE_PIN:
                    dora_list.append(SIX_PIN)
                elif indicator == RED_FIVE_SOU:
                    dora_list.append(SIX_SOU)
                else:
                    # if ONE_MAN < indicator < NINE_MAN
                    #     or indicator == RED_FIVE_MAN:
                    assert False, '2-8m does not exist in Sanma'
            else:
                if indicator == NINE_MAN:
                    dora_list.append(ONE_MAN)
                elif indicator == NINE_PIN:
                    dora_list.append(ONE_PIN)
                elif indicator == NINE_SOU:
                    dora_list.append(ONE_SOU)
                elif indicator == NORTH:
                    dora_list.append(EAST)
                elif indicator == CHUN:
                    dora_list.append(HAKU)
                elif indicator == RED_FIVE_MAN:
                    dora_list.append(SIX_MAN)
                elif indicator == RED_FIVE_PIN:
                    dora_list.append(SIX_PIN)
                elif indicator == RED_FIVE_SOU:
                    dora_list.append(SIX_SOU)
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
            dora_details.append({'han': dora_count, 'reason': Han.DORA})

        return dora_details, dora_count + red_dora_count + nuki_dora_count

    @staticmethod
    def calculate_han(hand, win_tile, win_group, melds=None, hand_config=None):
        """
        Calculate hand han with explanations (dora not counted)
        :param hand: List of 34-arrays
        :param win_tile: Integer index
        :param win_group: 34-array
        :param melds: List of Meld objects
        :param hand_config: HandConfig object
        :return: A list of han details, and an integer representing total
        number of han, and a Boolean indicating whether the hand is yakuman
        """
        if win_tile == RED_FIVE_MAN:
            win_tile = FIVE_MAN
        elif win_tile == RED_FIVE_PIN:
            win_tile = FIVE_PIN
        elif win_tile == RED_FIVE_SOU:
            win_tile = FIVE_SOU

        if not melds:
            melds = []

        open_melds = [item for item in melds
                      if item.type != Meld.KITA and item.is_open]
        hand_config.is_menzen = not bool(open_melds)

        yaku_list = []

        # HandConfig-related yaku

        # riichi, double riichi, and ippatsu
        if hand_config.yaku.double_riichi.is_condition_met(hand_config):
            yaku_list.append(hand_config.yaku.double_riichi)
            if hand_config.yaku.ippatsu.is_condition_met(hand_config):
                yaku_list.append(hand_config.yaku.ippatsu)
        elif hand_config.yaku.riichi.is_condition_met(hand_config):
            yaku_list.append(hand_config.yaku.riichi)
            if hand_config.yaku.ippatsu.is_condition_met(hand_config):
                yaku_list.append(hand_config.yaku.ippatsu)

        # menzen tsumo
        if hand_config.yaku.menzen_tsumo.is_condition_met(hand_config):
            yaku_list.append(hand_config.yaku.menzen_tsumo)

        # chankan and rinshan
        if hand_config.yaku.chankan.is_condition_met(hand_config):
            yaku_list.append(hand_config.yaku.chankan)
        elif hand_config.yaku.rinshan_kaihou.is_condition_met(hand_config):
            yaku_list.append(hand_config.yaku.rinshan_kaihou)

        # haitei and houtei
        if hand_config.yaku.haitei_raoyue.is_condition_met(hand_config):
            yaku_list.append(hand_config.yaku.haitei_raoyue)
        elif hand_config.yaku.houtei_raoyui.is_condition_met(hand_config):
            yaku_list.append(hand_config.yaku.houtei_raoyui)

        # tenhou, chiihou and nagashi mangan
        if hand_config.yaku.tenhou.is_condition_met(hand_config):
            yaku_list.append(hand_config.yaku.tenhou)
        elif hand_config.yaku.chiihou.is_condition_met(hand_config):
            yaku_list.append(hand_config.yaku.chiihou)
        elif hand_config.yaku.nagashi_mangan.is_condition_met(hand_config):
            return [{'han': 5,
                     'reason': hand_config.yaku.nagashi_mangan.name}], 5, False

        # kokushi musou and koukushi musou 13-men
        if isinstance(hand[0], int):
            if hand_config.yaku.kokushi_musou.is_condition_met(hand):
                if hand_config.yaku.kokushi_musou_13_men.is_condition_met(
                        hand, win_tile):
                    yaku_list.append(hand_config.yaku.kokushi_musou_13_men)
                else:
                    yaku_list.append(hand_config.yaku.kokushi_musou)
            else:
                return [], 0, False
        else:
            # chiitoitsu
            if hand_config.yaku.chiitoitsu.is_condition_met(hand):
                yaku_list.append(hand_config.yaku.chiitoitsu)

            # Standard hand (4 mentsu + 1 pair)
            else:
                shuntsu_set = [item for item in hand if Tiles.is_shuntsu(item)]
                koutsu_set = [item for item in hand
                              if Tiles.is_koutsu(item) or Tiles.is_kantsu(item)]

                # yaku that require at least one shuntsu
                if shuntsu_set:
                    # pinfu
                    if hand_config.yaku.pinfu.is_condition_met(
                            hand, win_tile, win_group, hand_config, melds):
                        yaku_list.append(hand_config.yaku.pinfu)

                    # ippeikou and ryanpeikou
                    if hand_config.yaku.ryanpeikou.is_condition_met(
                            hand, hand_config):
                        yaku_list.append(hand_config.yaku.ryanpeikou)
                    elif hand_config.yaku.iipeikou.is_condition_met(
                            hand, hand_config):
                        yaku_list.append(hand_config.yaku.iipeikou)

                    # chanta and junchan
                    if hand_config.yaku.junchan.is_condition_met(hand):
                        yaku_list.append(hand_config.yaku.junchan)
                    elif hand_config.yaku.chanta.is_condition_met(hand):
                        yaku_list.append(hand_config.yaku.chanta)

                    # ikkitsuukan
                    if hand_config.yaku.ikkitsuukan.is_condition_met(hand):
                        yaku_list.append(hand_config.yaku.ikkitsuukan)

                    # sanshoku doujun
                    if hand_config.yaku.sanshoku_doujun.is_condition_met(hand):
                        yaku_list.append(hand_config.yaku.sanshoku_doujun)

                # yaku that require at least one koutsu/kantsu
                if koutsu_set:
                    # yakuhai: seat wind
                    if hand_config.yaku.seat_wind.is_condition_met(
                            hand, hand_config):
                        yaku_list.append(hand_config.yaku.seat_wind)

                    # yakuhai: prevalent wind
                    if hand_config.yaku.prevalent_wind.is_condition_met(
                            hand, hand_config):
                        yaku_list.append(hand_config.yaku.prevalent_wind)

                    # yakuhai: haku
                    if hand_config.yaku.haku.is_condition_met(hand):
                        yaku_list.append(hand_config.yaku.haku)

                    # yakuhai: hatsu
                    if hand_config.yaku.hatsu.is_condition_met(hand):
                        yaku_list.append(hand_config.yaku.hatsu)

                    # yakuhai: chun
                    if hand_config.yaku.chun.is_condition_met(hand):
                        yaku_list.append(hand_config.yaku.chun)

                    # shousangen and daisangen
                    if hand_config.yaku.daisangen.is_condition_met(hand):
                        yaku_list.append(hand_config.yaku.daisangen)
                        yaku_list.remove(hand_config.yaku.haku)
                        yaku_list.remove(hand_config.yaku.hatsu)
                        yaku_list.remove(hand_config.yaku.chun)
                    elif hand_config.yaku.shousangen.is_condition_met(hand):
                        yaku_list.append(hand_config.yaku.shousangen)

                    # shousuushii and daisuushii
                    if hand_config.yaku.daisuushii.is_condition_met(hand):
                        yaku_list.append(hand_config.yaku.daisuushii)
                        if hand_config.yaku.seat_wind in yaku_list:
                            yaku_list.remove(hand_config.yaku.seat_wind)
                        if hand_config.yaku.prevalent_wind in yaku_list:
                            yaku_list.remove(hand_config.yaku.prevalent_wind)
                    elif hand_config.yaku.shousuushii.is_condition_met(hand):
                        yaku_list.append(hand_config.yaku.shousuushii)
                        if hand_config.yaku.seat_wind in yaku_list:
                            yaku_list.remove(hand_config.yaku.seat_wind)
                        if hand_config.yaku.prevalent_wind in yaku_list:
                            yaku_list.remove(hand_config.yaku.prevalent_wind)

                    # sanshoku doukou
                    if hand_config.yaku.sanshoku_doukou.is_condition_met(hand):
                        yaku_list.append(hand_config.yaku.sanshoku_doukou)

                    # toitoi
                    if hand_config.yaku.toitoihou.is_condition_met(hand):
                        yaku_list.append(hand_config.yaku.toitoihou)

                    # sanankou, suuankou, and suuankou tanki
                    if hand_config.yaku.suuankou_tanki.is_condition_met(
                            hand, win_tile, hand_config):
                        yaku_list.append(hand_config.yaku.suuankou_tanki)
                    elif hand_config.yaku.suuankou.is_condition_met(
                            hand, win_tile, hand_config):
                        yaku_list.append(hand_config.yaku.suuankou)
                    elif hand_config.yaku.sanankou.is_condition_met(
                            hand, win_tile, hand_config, melds):
                        yaku_list.append(hand_config.yaku.sanankou)

                    # sankantsu and suukantsu
                    if hand_config.yaku.suukantsu.is_condition_met(hand, melds):
                        yaku_list.append(hand_config.yaku.suukantsu)
                    elif hand_config.yaku.sankantsu.is_condition_met(hand,
                                                                     melds):
                        yaku_list.append(hand_config.yaku.sankantsu)

            # Tiles-related yaku (tanyao, chinitsu, etc.)

            # tanyao, chinroutou, and honroutou
            if hand_config.yaku.tanyao.is_condition_met(hand):
                yaku_list.append(hand_config.yaku.tanyao)
            elif hand_config.yaku.chinroutou.is_condition_met(hand):
                yaku_list.append(hand_config.yaku.chinroutou)
            elif hand_config.yaku.honroutou.is_condition_met(hand):
                yaku_list.append(hand_config.yaku.honroutou)

            # tsuuiisou
            if hand_config.yaku.tsuuiisou.is_condition_met(hand):
                yaku_list.append(hand_config.yaku.tsuuiisou)
            # ryuuiisou
            elif hand_config.yaku.ryuuiisou.is_condition_met(hand):
                yaku_list.append(hand_config.yaku.ryuuiisou)
            # chinitsu, chuuren poutou, and junsei chuuren poutou
            elif hand_config.yaku.chinitsu.is_condition_met(hand):
                # chuuren poutou and junsei chuuren poutou
                if hand_config.yaku.chuuren_poutou.is_condition_met(
                        hand, hand_config):
                    if hand_config.yaku.junsei_chuuren_poutou.is_condition_met(
                            hand, win_tile, hand_config):
                        yaku_list.append(hand_config.yaku.junsei_chuuren_poutou)
                    else:
                        yaku_list.append(hand_config.yaku.chuuren_poutou)
                # chinitsu
                else:
                    yaku_list.append(hand_config.yaku.chinitsu)
            # honitsu
            elif hand_config.yaku.honitsu.is_condition_met(hand):
                yaku_list.append(hand_config.yaku.honitsu)

        # deal with yakuman
        is_yakuman = False
        yakuman_list = [item for item in yaku_list if item.is_yakuman]
        if yakuman_list:
            yaku_list = yakuman_list
            is_yakuman = True

        # calculate han
        han_details = []
        han_value = 0

        if hand_config.is_menzen:
            for yaku in yaku_list:
                han_details.append({'han': yaku.han_closed,
                                    'reason': yaku.name})
                han_value += yaku.han_closed
        else:
            for yaku in yaku_list:
                if yaku.han_open is not None:
                    han_details.append({'han': yaku.han_open,
                                        'reason': yaku.name})
                    han_value += yaku.han_open

        return han_details, han_value, is_yakuman
