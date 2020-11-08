from hand_calculation.meld import Meld
from hand_calculation.tile_constants import ONE_MAN, FIVE_MAN, NINE_MAN, \
    ONE_PIN, FIVE_PIN, NINE_PIN, ONE_SOU, FIVE_SOU, NINE_SOU, RED_FIVE_MAN, \
    RED_FIVE_PIN, RED_FIVE_SOU, TERMINALS, DRAGONS, YAOCHUUHAI
from hand_calculation.tiles import Tiles


class FuCalculator:
    BASE = 'Base'
    MENZEN_RON = 'Menzen ron'
    CHIITOITSU = 'Chiitoitsu'

    EDGE_WAIT = 'Edge wait'
    CLOSED_WAIT = 'Closed wait'
    PAIR_WAIT = 'Pair wait'
    TSUMO = 'Tsumo'
    OPEN_PINFU = 'Open pinfu'

    PLAYER_WIND_PAIR = 'Seat wind pair'
    ROUND_WIND_PAIR = 'Prevalent wind pair'
    DRAGON_PAIR = 'Dragon pair'

    OPEN_KOUTSU = 'Open koutsu'
    OPEN_YAOCHUU_KOUTSU = 'Open yaochuuhai koutsu'
    CLOSED_KOUTSU = 'Closed koutsu'
    CLOSED_YAOCHUU_KOUTSU = 'Closed yaochuuhai koutsu'

    OPEN_KANTSU = 'Open kantsu'
    OPEN_YAOCHUU_KANTSU = 'Open yaochuuhai kantsu'
    CLOSED_KANTSU = 'Closed kantsu'
    CLOSED_YAOCHUU_KANTSU = 'Closed yaochuuhai kantsu'

    @staticmethod
    def calculate_fu(hand, win_tile, win_group, hand_config, melds=None):
        """
        Calculate hand fu with explanations
        :param hand: List of 34-arrays
        :param win_tile: Integer index
        :param win_group: 34-array containing the group where the winning tile
        is in
        :param hand_config: HandConfig object
        :param melds: Meld object
        :return: A list of fu details, and an integer total fu value
        """

        def contains_terminals(tile_indices):
            """
            :param tile_indices: List of integer indices
            :return: Boolean
            """
            return any([i in TERMINALS for i in tile_indices])

        if win_tile == RED_FIVE_MAN:
            win_tile = FIVE_MAN
        elif win_tile == RED_FIVE_PIN:
            win_tile = FIVE_PIN
        elif win_tile == RED_FIVE_SOU:
            win_tile = FIVE_SOU

        if not melds:
            melds = []

        # case of chiitoitsu
        if len(hand) == 7:
            return [{'fu': 25, 'reason': FuCalculator.CHIITOITSU}], 25

        fu_details = []

        # detect edge/closed wait
        open_shuntsu_set = [item.tiles for item in melds
                            if item.type == Meld.CHII]
        closed_shuntsu_set = []
        for item in hand:
            if Tiles.is_shuntsu(item):
                if item not in open_shuntsu_set:
                    closed_shuntsu_set.append(item)
                else:
                    open_shuntsu_set.remove(item)

        if win_group in closed_shuntsu_set:
            if ONE_MAN <= win_tile <= NINE_MAN:
                win_tile_index = win_tile % ONE_MAN
            elif ONE_PIN <= win_tile <= NINE_PIN:
                win_tile_index = win_tile % ONE_PIN
            elif ONE_SOU <= win_tile <= NINE_SOU:
                win_tile_index = win_tile % ONE_SOU
            else:
                assert False, 'Honour tiles cannot form shuntsu'

            win_group_indices = Tiles.array_to_indices(win_group)

            # edge wait
            if contains_terminals(win_group_indices):
                # 12 in hand, waiting for 3
                if win_tile_index == 2 \
                        and win_group_indices.index(win_tile) == 2:
                    fu_details.append({'fu': 2,
                                       'reason': FuCalculator.EDGE_WAIT})
                # 89 in hand, waiting for 7
                elif win_tile_index == 6 \
                        and win_group_indices.index(win_tile) == 0:
                    fu_details.append({'fu': 2,
                                       'reason': FuCalculator.EDGE_WAIT})

            # closed wait
            if win_group_indices.index(win_tile) == 1:
                fu_details.append({'fu': 2, 'reason': FuCalculator.CLOSED_WAIT})

        # detect pair wait
        if Tiles.is_pair(win_group):
            fu_details.append({'fu': 2, 'reason': FuCalculator.PAIR_WAIT})

        pair_index = -1
        for item in hand:
            if Tiles.is_pair(item):
                pair_index = Tiles.array_to_indices(item)[0]
                break
        assert pair_index != -1, 'Pair not found in hand'

        # detect seat wind pair
        if pair_index == hand_config.player_wind:
            fu_details.append({'fu': 2,
                               'reason': FuCalculator.PLAYER_WIND_PAIR})

        # detect prevalent wind pair:
        if pair_index == hand_config.round_wind:
            fu_details.append({'fu': 2,
                               'reason': FuCalculator.ROUND_WIND_PAIR})

        # detect dragon wind pair:
        if pair_index in DRAGONS:
            fu_details.append({'fu': 2, 'reason': FuCalculator.DRAGON_PAIR})

        open_melds = [item.tiles for item in melds if item.is_open]
        if not hand_config.is_tsumo:
            open_melds.append(win_group)

        # detect koutsu
        koutsu_set = [item for item in hand if Tiles.is_koutsu(item)]
        for koutsu in koutsu_set:
            koutsu_index = Tiles.array_to_indices(koutsu)[0]
            if koutsu in open_melds:
                if koutsu_index in YAOCHUUHAI:
                    fu_details.append({
                        'fu': 4,
                        'reason': FuCalculator.OPEN_YAOCHUU_KOUTSU
                    })
                else:
                    fu_details.append({
                        'fu': 2,
                        'reason': FuCalculator.OPEN_KOUTSU
                    })
            else:
                if koutsu_index in YAOCHUUHAI:
                    fu_details.append({
                        'fu': 8,
                        'reason': FuCalculator.CLOSED_YAOCHUU_KOUTSU
                    })
                else:
                    fu_details.append({
                        'fu': 4,
                        'reason': FuCalculator.CLOSED_KOUTSU
                    })

        # detect kantsu
        kantsu_set = [item for item in hand if Tiles.is_kantsu(item)]
        for kantsu in kantsu_set:
            kantsu_index = Tiles.array_to_indices(kantsu)[0]
            if kantsu in open_melds:
                if kantsu_index in YAOCHUUHAI:
                    fu_details.append({
                        'fu': 16,
                        'reason': FuCalculator.OPEN_YAOCHUU_KANTSU
                    })
                else:
                    fu_details.append({
                        'fu': 8,
                        'reason': FuCalculator.OPEN_KANTSU
                    })
            else:
                if kantsu_index in YAOCHUUHAI:
                    fu_details.append({
                        'fu': 32,
                        'reason': FuCalculator.CLOSED_YAOCHUU_KANTSU
                    })
                else:
                    fu_details.append({
                        'fu': 16,
                        'reason': FuCalculator.CLOSED_KANTSU
                    })

        # 2 fu for tsumo (except in the case of pinfu)
        if hand_config.is_tsumo and fu_details:
            fu_details.append({'fu': 2, 'reason': FuCalculator.TSUMO})

        is_open_hand = any([item.is_open for item in melds])

        # 2 fu for open pinfu
        if is_open_hand and (not fu_details):
            fu_details.append({'fu': 2, 'reason': FuCalculator.OPEN_PINFU})

        # add base fu and fu by menzen-ron
        fu_details.append({'fu': 20, 'reason': FuCalculator.BASE})
        if (not is_open_hand) and (not hand_config.is_tsumo):
            fu_details.append({'fu': 10, 'reason': FuCalculator.MENZEN_RON})

        fu_value = sum([item['fu'] for item in fu_details])
        fu_value = (fu_value + 9) // 10 * 10

        return fu_details, fu_value
