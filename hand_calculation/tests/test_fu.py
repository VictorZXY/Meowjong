import unittest

from hand_calculation import tile_constants
from hand_calculation.fu import Fu
from hand_calculation.hand_config import HandConfig
from hand_calculation.hand_divider import HandDivider
from hand_calculation.meld import Meld
from hand_calculation.tiles import Tiles


class FuTestCase(unittest.TestCase):
    def __get_win_groups(self, hand, win_tile):
        return [item for item in hand if item[win_tile] > 0]

    def __get_win_group(self, hand, win_tile):
        return self.__get_win_groups(hand, win_tile)[0]

    def __make_meld(self, meld_type=None, man='', pin='', sou='', honours='',
                    is_open=True):
        return Meld(meld_type,
                    tiles=Tiles.string_to_array(man, pin, sou, honours),
                    is_open=is_open)

    def __make_hand(self, private_tiles, win_tile, melds=None):
        private_tiles[win_tile] += 1
        hand_divider = HandDivider()
        return hand_divider.divide_hand(private_tiles, melds)[0]

    def test_chiitoitsu_fu(self):
        fu_calculator = Fu()
        hand_config = HandConfig()

        private_tiles = Tiles.string_to_array(man="115599", pin="6",
                                              sou="112244")
        win_tile = tile_constants.SIX_PIN
        hand = self.__make_hand(private_tiles, win_tile)
        win_group = self.__get_win_group(hand, win_tile)

        fu_details, fu = fu_calculator.calculate_fu(hand, win_tile, win_group,
                                                    hand_config)
        self.assertEqual(1, len(fu_details))
        self.assertTrue({"fu": 25, "reason": Fu.CHIITOITSU} in fu_details)
        self.assertEqual(fu, 25)

    def test_open_hand_base_fu(self):
        fu_calculator = Fu()
        hand_config = HandConfig()

        private_tiles = Tiles.string_to_array(man="123456", pin="11", sou="78")
        win_tile = tile_constants.SIX_SOU
        melds = [self.__make_meld(Meld.PON, sou="222")]
        hand = self.__make_hand(private_tiles, win_tile, melds)

        fu_details, fu = fu_calculator.calculate_fu(
            hand, win_tile, self.__get_win_group(hand, win_tile), hand_config,
            melds=melds
        )
        self.assertEqual(2, len(fu_details))
        self.assertTrue({"fu": 20, "reason": Fu.BASE} in fu_details)
        self.assertTrue({"fu": 2, "reason": Fu.OPEN_KOUTSU} in fu_details)
        self.assertEqual(fu, 30)

    def test_fu_based_on_different_win_groups(self):
        fu_calculator = Fu()
        hand_config = HandConfig()

        private_tiles = Tiles.string_to_array(man="234789", pin="1234566")
        win_tile = tile_constants.SIX_PIN
        hand = self.__make_hand(private_tiles, win_tile)
        win_groups = self.__get_win_groups(hand, win_tile)

        # pinfu wait 456
        fu_details, fu = fu_calculator.calculate_fu(hand, win_tile,
                                                    win_groups[0], hand_config)
        self.assertEqual(fu, 30)

        # pair wait 66
        fu_details, fu = fu_calculator.calculate_fu(hand, win_tile,
                                                    win_groups[1], hand_config)
        self.assertEqual(fu, 40)

    def test_open_pinfu_fu(self):
        fu_calculator = Fu()
        hand_config = HandConfig()

        private_tiles = Tiles.string_to_array(man="234567", pin="22", sou="78")
        win_tile = tile_constants.SIX_SOU
        melds = [self.__make_meld(Meld.CHII, sou="234")]
        hand = self.__make_hand(private_tiles, win_tile, melds)

        fu_details, fu = fu_calculator.calculate_fu(
            hand, win_tile, self.__get_win_group(hand, win_tile), hand_config,
            melds=melds
        )
        self.assertEqual(2, len(fu_details))
        self.assertTrue({"fu": 20, "reason": Fu.BASE} in fu_details)
        self.assertTrue({"fu": 2, "reason": Fu.OPEN_PINFU} in fu_details)
        self.assertEqual(fu, 30)

    def test_tsumo_base_fu(self):
        fu_calculator = Fu()
        hand_config = HandConfig()

        private_tiles = Tiles.string_to_array(man="123456", pin="11",
                                              sou="22278")
        win_tile = tile_constants.SIX_SOU
        hand = self.__make_hand(private_tiles, win_tile)

        fu_details, _ = fu_calculator.calculate_fu(
            hand, win_tile, self.__get_win_group(hand, win_tile), hand_config)
        self.assertTrue({"fu": 20, "reason": Fu.BASE} in fu_details)

    def test_tsumo_pinfu_fu(self):
        fu_calculator = Fu()
        hand_config = HandConfig(is_tsumo=True)

        private_tiles = Tiles.string_to_array(man="123456", pin="123",
                                              sou="2278")
        win_tile = tile_constants.SIX_SOU
        hand = self.__make_hand(private_tiles, win_tile)

        fu_details, fu = fu_calculator.calculate_fu(
            hand, win_tile, self.__get_win_group(hand, win_tile), hand_config)
        self.assertEqual(1, len(fu_details))
        self.assertTrue({"fu": 20, "reason": Fu.BASE} in fu_details)
        self.assertEqual(fu, 20)

    def test_tsumo_fu(self):
        fu_calculator = Fu()
        hand_config = HandConfig(is_tsumo=True)

        private_tiles = Tiles.string_to_array(man="123456", pin="111",
                                              sou="2278")
        win_tile = tile_constants.SIX_SOU
        hand = self.__make_hand(private_tiles, win_tile)

        fu_details, fu = fu_calculator.calculate_fu(
            hand, win_tile, self.__get_win_group(hand, win_tile), hand_config)
        self.assertTrue({"fu": 20, "reason": Fu.BASE} in fu_details)
        self.assertTrue({"fu": 2, "reason": Fu.TSUMO} in fu_details)
        self.assertEqual(fu, 30)

    def test_edge_wait_fu(self):
        fu_calculator = Fu()
        hand_config = HandConfig()

        # 12 in hand, waiting for 3
        private_tiles = Tiles.string_to_array(man="123456", pin="55",
                                              sou="12456")
        win_tile = tile_constants.THREE_SOU
        hand = self.__make_hand(private_tiles, win_tile)

        fu_details, fu = fu_calculator.calculate_fu(
            hand, win_tile, self.__get_win_group(hand, win_tile), hand_config)
        self.assertEqual(3, len(fu_details))
        self.assertTrue({"fu": 20, "reason": Fu.BASE} in fu_details)
        self.assertTrue({"fu": 10, "reason": Fu.MENZEN_RON} in fu_details)
        self.assertTrue({"fu": 2, "reason": Fu.EDGE_WAIT} in fu_details)
        self.assertEqual(fu, 40)

        # 89 in hand, waiting for 7
        private_tiles = Tiles.string_to_array(man="123456", pin="55",
                                              sou="34589")
        win_tile = tile_constants.SEVEN_SOU
        hand = self.__make_hand(private_tiles, win_tile)

        fu_details, fu = fu_calculator.calculate_fu(
            hand, win_tile, self.__get_win_group(hand, win_tile), hand_config)
        self.assertEqual(3, len(fu_details))
        self.assertTrue({"fu": 20, "reason": Fu.BASE} in fu_details)
        self.assertTrue({"fu": 10, "reason": Fu.MENZEN_RON} in fu_details)
        self.assertTrue({"fu": 2, "reason": Fu.EDGE_WAIT} in fu_details)
        self.assertEqual(fu, 40)

    def test_closed_wait_fu(self):
        fu_calculator = Fu()
        hand_config = HandConfig()

        private_tiles = Tiles.string_to_array(man="123456", pin="55",
                                              sou="12357")
        win_tile = tile_constants.SIX_SOU
        hand = self.__make_hand(private_tiles, win_tile)

        fu_details, fu = fu_calculator.calculate_fu(
            hand, win_tile, self.__get_win_group(hand, win_tile), hand_config)
        self.assertEqual(3, len(fu_details))
        self.assertTrue({"fu": 20, "reason": Fu.BASE} in fu_details)
        self.assertTrue({"fu": 10, "reason": Fu.MENZEN_RON} in fu_details)
        self.assertTrue({"fu": 2, "reason": Fu.CLOSED_WAIT} in fu_details)
        self.assertEqual(fu, 40)

    def test_pair_wait_fu(self):
        fu_calculator = Fu()
        hand_config = HandConfig()

        private_tiles = Tiles.string_to_array(man="123456", pin="1",
                                              sou="123678")
        win_tile = tile_constants.ONE_PIN
        hand = self.__make_hand(private_tiles, win_tile)

        fu_details, fu = fu_calculator.calculate_fu(
            hand, win_tile, self.__get_win_group(hand, win_tile), hand_config)
        self.assertEqual(3, len(fu_details))
        self.assertTrue({"fu": 20, "reason": Fu.BASE} in fu_details)
        self.assertTrue({"fu": 10, "reason": Fu.MENZEN_RON} in fu_details)
        self.assertTrue({"fu": 2, "reason": Fu.PAIR_WAIT} in fu_details)
        self.assertEqual(fu, 40)

    def test_valued_pair_fu(self):
        # player wind pair
        fu_calculator = Fu()
        hand_config = HandConfig(player_wind=tile_constants.EAST)

        private_tiles = Tiles.string_to_array(man="123456", sou="12378",
                                              honours="11")
        win_tile = tile_constants.SIX_SOU
        hand = self.__make_hand(private_tiles, win_tile)

        fu_details, fu = fu_calculator.calculate_fu(
            hand, win_tile, self.__get_win_group(hand, win_tile), hand_config)
        self.assertEqual(3, len(fu_details))
        self.assertTrue({"fu": 20, "reason": Fu.BASE} in fu_details)
        self.assertTrue({"fu": 10, "reason": Fu.MENZEN_RON} in fu_details)
        self.assertTrue({"fu": 2, "reason": Fu.PLAYER_WIND_PAIR} in fu_details)
        self.assertEqual(fu, 40)

        # round wind pair
        hand_config = HandConfig(round_wind=tile_constants.EAST)
        fu_details, fu = fu_calculator.calculate_fu(
            hand, win_tile, self.__get_win_group(hand, win_tile), hand_config)
        self.assertEqual(3, len(fu_details))
        self.assertTrue({"fu": 20, "reason": Fu.BASE} in fu_details)
        self.assertTrue({"fu": 10, "reason": Fu.MENZEN_RON}
                        in fu_details)
        self.assertTrue({"fu": 2, "reason": Fu.ROUND_WIND_PAIR}
                        in fu_details)
        self.assertEqual(fu, 40)

        # double wind pair
        hand_config = HandConfig(player_wind=tile_constants.EAST,
                                 round_wind=tile_constants.EAST)
        fu_details, fu = fu_calculator.calculate_fu(
            hand, win_tile, self.__get_win_group(hand, win_tile), hand_config)
        self.assertEqual(4, len(fu_details))
        self.assertTrue({"fu": 20, "reason": Fu.BASE} in fu_details)
        self.assertTrue({"fu": 10, "reason": Fu.MENZEN_RON} in fu_details)
        self.assertTrue({"fu": 2, "reason": Fu.PLAYER_WIND_PAIR} in fu_details)
        self.assertTrue({"fu": 2, "reason": Fu.ROUND_WIND_PAIR} in fu_details)
        self.assertEqual(fu, 40)

        # dragon pair
        hand_config = HandConfig()

        private_tiles = Tiles.string_to_array(man="123456", sou="12378",
                                              honours="77")
        win_tile = tile_constants.SIX_SOU
        hand = self.__make_hand(private_tiles, win_tile)

        fu_details, fu = fu_calculator.calculate_fu(
            hand, win_tile, self.__get_win_group(hand, win_tile), hand_config)
        self.assertEqual(3, len(fu_details))
        self.assertTrue({"fu": 20, "reason": Fu.BASE} in fu_details)
        self.assertTrue({"fu": 10, "reason": Fu.MENZEN_RON} in fu_details)
        self.assertTrue({"fu": 2, "reason": Fu.DRAGON_PAIR} in fu_details)
        self.assertEqual(fu, 40)

    def test_open_koutsu_fu(self):
        fu_calculator = Fu()
        hand_config = HandConfig()

        private_tiles = Tiles.string_to_array(man="123456", pin="11", sou="78")
        win_tile = tile_constants.SIX_SOU
        melds = [self.__make_meld(Meld.PON, sou="222")]
        hand = self.__make_hand(private_tiles, win_tile, melds)

        fu_details, fu = fu_calculator.calculate_fu(
            hand, win_tile, self.__get_win_group(hand, win_tile), hand_config,
            melds=melds
        )
        self.assertEqual(2, len(fu_details))
        self.assertTrue({"fu": 20, "reason": Fu.BASE} in fu_details)
        self.assertTrue({"fu": 2, "reason": Fu.OPEN_KOUTSU} in fu_details)
        self.assertEqual(fu, 30)

    def test_closed_koutsu_fu(self):
        fu_calculator = Fu()
        hand_config = HandConfig()

        private_tiles = Tiles.string_to_array(man="123456", pin="11",
                                              sou="22278")
        win_tile = tile_constants.SIX_SOU
        hand = self.__make_hand(private_tiles, win_tile)

        fu_details, fu = fu_calculator.calculate_fu(
            hand, win_tile, self.__get_win_group(hand, win_tile), hand_config)
        self.assertEqual(3, len(fu_details))
        self.assertTrue({"fu": 20, "reason": Fu.BASE} in fu_details)
        self.assertTrue({"fu": 10, "reason": Fu.MENZEN_RON} in fu_details)
        self.assertTrue({"fu": 4, "reason": Fu.CLOSED_KOUTSU} in fu_details)
        self.assertEqual(fu, 40)

        # when we ron on the third koutsu tile, we consider the koutsu as open
        private_tiles = Tiles.string_to_array(man="123456", pin="11",
                                              sou="22678")
        win_tile = tile_constants.TWO_SOU
        hand = self.__make_hand(private_tiles, win_tile)

        fu_details, fu = fu_calculator.calculate_fu(
            hand, win_tile, self.__get_win_group(hand, win_tile), hand_config)
        self.assertEqual(3, len(fu_details))
        self.assertTrue({"fu": 20, "reason": Fu.BASE} in fu_details)
        self.assertTrue({"fu": 10, "reason": Fu.MENZEN_RON} in fu_details)
        self.assertTrue({"fu": 2, "reason": Fu.OPEN_KOUTSU} in fu_details)
        self.assertEqual(fu, 40)

    def test_open_yaochuuhai_koutsu_fu(self):
        fu_calculator = Fu()
        hand_config = HandConfig()

        private_tiles = Tiles.string_to_array(man="123456", sou="2278")
        win_tile = tile_constants.SIX_SOU
        melds = [self.__make_meld(Meld.PON, honours="111")]
        hand = self.__make_hand(private_tiles, win_tile, melds)

        fu_details, fu = fu_calculator.calculate_fu(
            hand, win_tile, self.__get_win_group(hand, win_tile), hand_config,
            melds=melds
        )
        self.assertEqual(2, len(fu_details))
        self.assertTrue({"fu": 20, "reason": Fu.BASE} in fu_details)
        self.assertTrue({"fu": 4, "reason": Fu.OPEN_YAOCHUU_KOUTSU}
                        in fu_details)
        self.assertEqual(fu, 30)

    def test_closed_terminal_koutsu_fu(self):
        fu_calculator = Fu()
        hand_config = HandConfig()

        private_tiles = Tiles.string_to_array(man="123456", pin="11",
                                              sou="11178")
        win_tile = tile_constants.SIX_SOU
        hand = self.__make_hand(private_tiles, win_tile)

        fu_details, fu = fu_calculator.calculate_fu(
            hand, win_tile, self.__get_win_group(hand, win_tile), hand_config)
        self.assertEqual(3, len(fu_details))
        self.assertTrue({"fu": 20, "reason": Fu.BASE} in fu_details)
        self.assertTrue({"fu": 10, "reason": Fu.MENZEN_RON} in fu_details)
        self.assertTrue({"fu": 8, "reason": Fu.CLOSED_YAOCHUU_KOUTSU}
                        in fu_details)
        self.assertEqual(fu, 40)

        # when we ron on the third koutsu tile, we consider the koutsu as open
        private_tiles = Tiles.string_to_array(man="123456", pin="11",
                                              sou="11678")
        win_tile = tile_constants.ONE_SOU
        hand = self.__make_hand(private_tiles, win_tile)

        fu_details, fu = fu_calculator.calculate_fu(
            hand, win_tile, self.__get_win_group(hand, win_tile), hand_config)
        self.assertEqual(3, len(fu_details))
        self.assertTrue({"fu": 20, "reason": Fu.BASE} in fu_details)
        self.assertTrue({"fu": 10, "reason": Fu.MENZEN_RON} in fu_details)
        self.assertTrue({"fu": 4, "reason": Fu.OPEN_YAOCHUU_KOUTSU}
                        in fu_details)
        self.assertEqual(fu, 40)

    def test_closed_honour_koutsu_fu(self):
        fu_calculator = Fu()
        hand_config = HandConfig()

        private_tiles = Tiles.string_to_array(man="123456", sou="1178",
                                              honours="111")
        win_tile = tile_constants.SIX_SOU
        hand = self.__make_hand(private_tiles, win_tile)

        fu_details, fu = fu_calculator.calculate_fu(
            hand, win_tile, self.__get_win_group(hand, win_tile), hand_config)
        self.assertEqual(3, len(fu_details))
        self.assertTrue({"fu": 20, "reason": Fu.BASE} in fu_details)
        self.assertTrue({"fu": 10, "reason": Fu.MENZEN_RON} in fu_details)
        self.assertTrue({"fu": 8, "reason": Fu.CLOSED_YAOCHUU_KOUTSU}
                        in fu_details)
        self.assertEqual(fu, 40)

        # when we ron on the third pon tile we consider pon as open
        private_tiles = Tiles.string_to_array(man="123456", sou="11678",
                                              honours="11")
        win_tile = tile_constants.EAST
        hand = self.__make_hand(private_tiles, win_tile)

        fu_details, fu = fu_calculator.calculate_fu(
            hand, win_tile, self.__get_win_group(hand, win_tile), hand_config)
        self.assertEqual(3, len(fu_details))
        self.assertTrue({"fu": 20, "reason": Fu.BASE} in fu_details)
        self.assertTrue({"fu": 10, "reason": Fu.MENZEN_RON} in fu_details)
        self.assertTrue({"fu": 4, "reason": Fu.OPEN_YAOCHUU_KOUTSU}
                        in fu_details)
        self.assertEqual(fu, 40)

    def test_open_kantsu_fu(self):
        fu_calculator = Fu()
        hand_config = HandConfig()

        private_tiles = Tiles.string_to_array(man="123456", pin="11", sou="78")
        win_tile = tile_constants.SIX_SOU
        melds = [self.__make_meld(Meld.KAN, sou="2222", is_open=True)]
        hand = self.__make_hand(private_tiles, win_tile, melds)

        fu_details, fu = fu_calculator.calculate_fu(
            hand, win_tile, self.__get_win_group(hand, win_tile), hand_config,
            melds=melds
        )
        self.assertEqual(2, len(fu_details))
        self.assertTrue({"fu": 20, "reason": Fu.BASE} in fu_details)
        self.assertTrue({"fu": 8, "reason": Fu.OPEN_KANTSU} in fu_details)
        self.assertEqual(fu, 30)

    def test_closed_kantsu_fu(self):
        fu_calculator = Fu()
        hand_config = HandConfig()

        private_tiles = Tiles.string_to_array(man="123456", pin="11", sou="78")
        win_tile = tile_constants.SIX_SOU
        melds = [self.__make_meld(Meld.KAN, sou="2222", is_open=False)]
        hand = self.__make_hand(private_tiles, win_tile, melds)

        fu_details, fu = fu_calculator.calculate_fu(
            hand, win_tile, self.__get_win_group(hand, win_tile), hand_config,
            melds=melds
        )
        self.assertEqual(3, len(fu_details))
        self.assertTrue({"fu": 20, "reason": Fu.BASE} in fu_details)
        self.assertTrue({"fu": 10, "reason": Fu.MENZEN_RON} in fu_details)
        self.assertTrue({"fu": 16, "reason": Fu.CLOSED_KANTSU} in fu_details)
        self.assertEqual(fu, 50)

    def test_open_yaochuuhai_kantsu_fu(self):
        fu_calculator = Fu()
        hand_config = HandConfig()

        private_tiles = Tiles.string_to_array(man="123456", sou="2278")
        win_tile = tile_constants.SIX_SOU
        melds = [self.__make_meld(Meld.KAN, pin="1111")]
        hand = self.__make_hand(private_tiles, win_tile, melds)

        fu_details, fu = fu_calculator.calculate_fu(
            hand, win_tile, self.__get_win_group(hand, win_tile), hand_config,
            melds=melds
        )
        self.assertEqual(2, len(fu_details))
        self.assertTrue({"fu": 20, "reason": Fu.BASE} in fu_details)
        self.assertTrue({"fu": 16, "reason": Fu.OPEN_YAOCHUU_KANTSU}
                        in fu_details)
        self.assertEqual(fu, 40)

    def test_closed_yaochuuhai_kantsu_fu(self):
        fu_calculator = Fu()
        hand_config = HandConfig()

        private_tiles = Tiles.string_to_array(man="123456", sou="2278")
        win_tile = tile_constants.SIX_SOU
        melds = [self.__make_meld(Meld.KAN, pin="1111", is_open=False)]
        hand = self.__make_hand(private_tiles, win_tile, melds)

        fu_details, fu = fu_calculator.calculate_fu(
            hand, win_tile, self.__get_win_group(hand, win_tile), hand_config,
            melds=melds
        )
        self.assertEqual(3, len(fu_details))
        self.assertTrue({"fu": 20, "reason": Fu.BASE} in fu_details)
        self.assertTrue({"fu": 10, "reason": Fu.MENZEN_RON} in fu_details)
        self.assertTrue({"fu": 32, "reason": Fu.CLOSED_YAOCHUU_KANTSU}
                        in fu_details)
        self.assertEqual(fu, 70)


if __name__ == '__main__':
    unittest.main()
