import unittest

from hand_calculation.hand_calculator import HandCalculator
from hand_calculation.hand_config import HandConfig
from hand_calculation.hand_divider import HandDivider
from hand_calculation.meld import Meld
from hand_calculation.tile_constants import ONE_MAN, ONE_PIN, ONE_SOU, EAST, \
    RED_FIVE_MAN, RED_FIVE_PIN, RED_FIVE_SOU
from hand_calculation.tiles import Tiles
from hand_calculation.yaku_config import YakuConfig


class HandCalculatorYakumanTestCase(unittest.TestCase):
    def __string_to_tile_index(self, man='', pin='', sou='', honours=''):
        if man != '':
            if man == '0':
                return RED_FIVE_MAN
            else:
                return int(man) + ONE_MAN - 1
        elif pin != '':
            if pin == '0':
                return RED_FIVE_PIN
            else:
                return int(pin) + ONE_PIN - 1
        elif sou != '':
            if sou == '0':
                return RED_FIVE_SOU
            else:
                return int(sou) + ONE_SOU - 1
        else:
            return int(honours) + EAST - 1

    def __make_meld(self, meld_type=None, man='', pin='', sou='', honours='',
                    is_open=True):
        return Meld(meld_type,
                    tiles=Tiles.string_to_array(man=man, pin=pin, sou=sou,
                                                honours=honours),
                    is_open=is_open)

    def test_tenhou(self):
        tiles = Tiles.string_to_array(sou="12344", man="234456", pin="66")
        win_tile = self.__string_to_tile_index(sou="4")
        result = HandCalculator.calculate_hand_score(
            tiles, win_tile, hand_config=HandConfig(is_tenhou=True))
        self.assertEqual(result['han'], 13)
        self.assertEqual(result['fu'], 30)
        self.assertEqual(len(result['han_details']), 1)

    def test_chiihou(self):
        tiles = Tiles.string_to_array(sou="12344", man="234456", pin="66")
        win_tile = self.__string_to_tile_index(sou="4")
        result = HandCalculator.calculate_hand_score(
            tiles, win_tile, hand_config=HandConfig(is_chiihou=True))
        self.assertEqual(result['han'], 13)
        self.assertEqual(result['fu'], 30)
        self.assertEqual(len(result['han_details']), 1)

    def test_daisangen(self):
        tiles = Tiles.string_to_array(sou="123", man="22", honours="55566677")
        win_tile = self.__string_to_tile_index(honours="7")
        result = HandCalculator.calculate_hand_score(tiles, win_tile)
        self.assertEqual(result['han'], 13)
        self.assertEqual(result['fu'], 50)
        self.assertEqual(len(result['han_details']), 1)

    def test_suuankou(self):
        tiles = Tiles.string_to_array(sou="111444", man="333", pin="4455")
        win_tile = self.__string_to_tile_index(pin="5")
        result = HandCalculator.calculate_hand_score(
            tiles, win_tile, hand_config=HandConfig(is_tsumo=True))
        self.assertEqual(result['han'], 13)
        self.assertEqual(result['fu'], 50)
        self.assertEqual(len(result['han_details']), 1)

        result = HandCalculator.calculate_hand_score(
            tiles, win_tile, hand_config=HandConfig(is_tsumo=False))
        self.assertNotEqual(result['han'], 13)

    def test_suuankou_tanki(self):
        tiles = Tiles.string_to_array(sou="111444", man="333", pin="4445")
        win_tile = self.__string_to_tile_index(pin="5")
        result = HandCalculator.calculate_hand_score(
            tiles, win_tile, hand_config=HandConfig(is_tsumo=True))
        self.assertEqual(result['han'], 26)
        self.assertEqual(result['fu'], 50)
        self.assertEqual(len(result['han_details']), 1)

        tiles = Tiles.string_to_array(man="3334445557779")
        win_tile = self.__string_to_tile_index(man="9")
        result = HandCalculator.calculate_hand_score(
            tiles, win_tile, hand_config=HandConfig(is_tsumo=False))
        self.assertEqual(result['han'], 26)
        self.assertEqual(result['fu'], 50)
        self.assertEqual(len(result['han_details']), 1)

    def test_tsuuiisou(self):
        yaku_config = YakuConfig()

        tiles = Tiles.string_to_array(honours="11122233366677")
        self.assertTrue(yaku_config.tsuuiisou.is_condition_met(
            HandDivider.divide_hand(tiles)[0]))

        tiles = Tiles.string_to_array(honours="11223344556677")
        self.assertTrue(yaku_config.tsuuiisou.is_condition_met(
            HandDivider.divide_hand(tiles)[0]))

        tiles = Tiles.string_to_array(honours="1133445577", pin="88", sou="11")
        self.assertFalse(yaku_config.tsuuiisou.is_condition_met(
            HandDivider.divide_hand(tiles)[0]))

        tiles = Tiles.string_to_array(honours="1122334455667")
        win_tile = self.__string_to_tile_index(honours="7")
        result = HandCalculator.calculate_hand_score(tiles, win_tile)
        self.assertEqual(result['han'], 13)
        self.assertEqual(result['fu'], 25)
        self.assertEqual(len(result['han_details']), 1)

    def test_ryuuiisou(self):
        yaku_config = YakuConfig()

        tiles = Tiles.string_to_array(sou="22334466888", honours="666")
        self.assertTrue(yaku_config.ryuuiisou.is_condition_met(
            HandDivider.divide_hand(tiles)[0]))

        tiles = Tiles.string_to_array(sou="22334466888", honours="66")
        win_tile = self.__string_to_tile_index(honours="6")
        result = HandCalculator.calculate_hand_score(tiles, win_tile)
        self.assertEqual(result['han'], 13)
        self.assertEqual(result['fu'], 40)
        self.assertEqual(len(result['han_details']), 1)

    def test_chinroutou(self):
        yaku_config = YakuConfig()

        tiles = Tiles.string_to_array(sou="111999", man="111999", pin="99")
        self.assertTrue(yaku_config.chinroutou.is_condition_met(
            HandDivider.divide_hand(tiles)[0]))

        tiles = Tiles.string_to_array(sou="111222", man="111999", pin="9")
        win_tile = self.__string_to_tile_index(pin="9")
        result = HandCalculator.calculate_hand_score(tiles, win_tile)
        self.assertEqual(result['han'], 26)
        self.assertEqual(result['fu'], 60)
        self.assertEqual(len(result['han_details']), 1)

    def test_kokushi_musou(self):
        yaku_config = YakuConfig()

        tiles = Tiles.string_to_array(sou="119", man="19", pin="19",
                                      honours="1234567")
        self.assertTrue(yaku_config.kokushi_musou.is_condition_met(tiles))

        tiles = Tiles.string_to_array(sou="11", man="19", pin="19",
                                      honours="1234567")
        win_tile = self.__string_to_tile_index(sou="9")
        result = HandCalculator.calculate_hand_score(tiles, win_tile)
        self.assertEqual(result['han'], 13)
        self.assertEqual(result['fu'], 0)
        self.assertEqual(len(result['han_details']), 1)

    def test_kokushi_musou_13_men(self):
        tiles = Tiles.string_to_array(sou="19", man="19", pin="19",
                                      honours="1234567")
        win_tile = self.__string_to_tile_index(sou="1")
        result = HandCalculator.calculate_hand_score(tiles, win_tile)
        self.assertEqual(result['han'], 26)
        self.assertEqual(result['fu'], 0)
        self.assertEqual(len(result['han_details']), 1)

    def test_shousuushii(self):
        yaku_config = YakuConfig()

        tiles = Tiles.string_to_array(sou="123", honours="11122233344")
        self.assertTrue(yaku_config.shousuushii.is_condition_met(
            HandDivider.divide_hand(tiles)[0]))

        tiles = Tiles.string_to_array(sou="123", honours="1112223334")
        win_tile = self.__string_to_tile_index(honours="4")
        result = HandCalculator.calculate_hand_score(tiles, win_tile)
        self.assertEqual(result['han'], 13)
        self.assertEqual(result['fu'], 60)
        self.assertEqual(len(result['han_details']), 1)

    def test_daisuushii(self):
        yaku_config = YakuConfig()

        tiles = Tiles.string_to_array(sou="22", honours="111222333444")
        self.assertTrue(yaku_config.daisuushii.is_condition_met(
            HandDivider.divide_hand(tiles)[0]))

        tiles = Tiles.string_to_array(sou="22", honours="11122233344")
        win_tile = self.__string_to_tile_index(honours="4")
        result = HandCalculator.calculate_hand_score(tiles, win_tile)
        self.assertEqual(result['han'], 26)
        self.assertEqual(result['fu'], 60)
        self.assertEqual(len(result['han_details']), 1)

    def test_suukantsu(self):
        yaku_config = YakuConfig()

        melds = [
            self.__make_meld(Meld.KAN, sou="1111"),
            self.__make_meld(Meld.KAN, sou="3333"),
            self.__make_meld(Meld.KAN, pin="5505", is_open=False),
            self.__make_meld(Meld.KAN, man="2222")
        ]
        self.assertTrue(yaku_config.suukantsu.is_condition_met(None, melds))

        tiles = Tiles.string_to_array(pin="4")
        win_tile = self.__string_to_tile_index(pin="4")
        melds = [
            self.__make_meld(Meld.KAN, sou="1111"),
            self.__make_meld(Meld.KAN, sou="3333"),
            self.__make_meld(Meld.KAN, pin="5505", is_open=False),
            self.__make_meld(Meld.KAN, man="2222")
        ]
        result = HandCalculator.calculate_hand_score(
            tiles, win_tile, melds=melds)
        self.assertEqual(result['han'], 13)
        self.assertEqual(result['fu'], 70)
        self.assertEqual(len(result['han_details']), 1)

    def test_chuuren_poutou(self):
        yaku_config = YakuConfig()
        hand_config = HandConfig(is_menzen=True)

        tiles = Tiles.string_to_array(man="11112345678999")
        self.assertTrue(yaku_config.chuuren_poutou.is_condition_met(
            HandDivider.divide_hand(tiles)[0], hand_config))

        tiles = Tiles.string_to_array(pin="11122345678999")
        self.assertTrue(yaku_config.chuuren_poutou.is_condition_met(
            HandDivider.divide_hand(tiles)[0], hand_config))

        tiles = Tiles.string_to_array(sou="11123345678999")
        self.assertTrue(yaku_config.chuuren_poutou.is_condition_met(
            HandDivider.divide_hand(tiles)[0], hand_config))

        tiles = Tiles.string_to_array(sou="11123445678999")
        self.assertTrue(yaku_config.chuuren_poutou.is_condition_met(
            HandDivider.divide_hand(tiles)[0], hand_config))

        tiles = Tiles.string_to_array(sou="11123455678999")
        self.assertTrue(yaku_config.chuuren_poutou.is_condition_met(
            HandDivider.divide_hand(tiles)[0], hand_config))

        tiles = Tiles.string_to_array(sou="11123456678999")
        self.assertTrue(yaku_config.chuuren_poutou.is_condition_met(
            HandDivider.divide_hand(tiles)[0], hand_config))

        tiles = Tiles.string_to_array(sou="11123456778999")
        self.assertTrue(yaku_config.chuuren_poutou.is_condition_met(
            HandDivider.divide_hand(tiles)[0], hand_config))

        tiles = Tiles.string_to_array(sou="11123456788999")
        self.assertTrue(yaku_config.chuuren_poutou.is_condition_met(
            HandDivider.divide_hand(tiles)[0], hand_config))

        tiles = Tiles.string_to_array(sou="11123456789999")
        self.assertTrue(yaku_config.chuuren_poutou.is_condition_met(
            HandDivider.divide_hand(tiles)[0], hand_config))

        tiles = Tiles.string_to_array(man="1123456789999")
        win_tile = self.__string_to_tile_index(man="1")
        result = HandCalculator.calculate_hand_score(tiles, win_tile)
        self.assertEqual(result['han'], 13)
        self.assertEqual(result['fu'], 40)
        self.assertEqual(len(result['han_details']), 1)

        tiles = Tiles.string_to_array(pin="1112456678")
        win_tile = self.__string_to_tile_index(pin="3")
        melds = [self.__make_meld(Meld.KAN, pin="9999", is_open=False)]
        result = HandCalculator.calculate_hand_score(
            tiles, win_tile, melds=melds)
        self.assertEqual(result['han'], 6)
        self.assertEqual(result['fu'], 70)
        self.assertEqual(len(result['han_details']), 1)

    def test_junsei_chuuren_poutou(self):
        tests = [
            ["1112345678999", "2"],
            ["1112345678999", "9"],
            ["1112345678999", "1"],
        ]
        for hand_tiles, win_tile in tests:
            tiles = Tiles.string_to_array(man=hand_tiles)
            win_tile = self.__string_to_tile_index(man=win_tile)
            result = HandCalculator.calculate_hand_score(tiles, win_tile)
            self.assertEqual(result['han'], 26)
            self.assertEqual(len(result['han_details']), 1)

    def test_5x_yakuman(self):
        tiles = Tiles.string_to_array(honours="5")
        win_tile = self.__string_to_tile_index(honours="5")
        melds = [
            self.__make_meld(Meld.KAN, honours="1111", is_open=False),
            self.__make_meld(Meld.KAN, honours="3333", is_open=False),
            self.__make_meld(Meld.KAN, honours="4444", is_open=False),
            self.__make_meld(Meld.KAN, honours="2222", is_open=False)
        ]
        hand_config = HandConfig(is_tenhou=True)
        result = HandCalculator.calculate_hand_score(
            tiles, win_tile, melds=melds, hand_config=hand_config)
        self.assertEqual(result['han'], 91)
        self.assertEqual(result["score"], 240000)

    def test_kokushi_musou_multiple_yakuman(self):
        # kokushi musou tests

        tiles = Tiles.string_to_array(sou="19", pin="19", man="19",
                                      honours="2345677")
        win_tile = self.__string_to_tile_index(honours="1")
        hand_config = HandConfig(is_tsumo=True,
                                 is_tenhou=False,
                                 is_chiihou=False)
        result = HandCalculator.calculate_hand_score(
            tiles, win_tile, hand_config=hand_config)
        self.assertEqual(len(result['han_details']), 1)
        self.assertTrue(
            {'han': 13, 'reason': hand_config.yaku.kokushi_musou.name}
            in result['han_details'])
        self.assertFalse(
            {'han': 26, 'reason': hand_config.yaku.kokushi_musou_13_men.name}
            in result['han_details'])
        self.assertFalse(
            {'han': 13, 'reason': hand_config.yaku.tenhou.name}
            in result['han_details'])
        self.assertFalse(
            {'han': 13, 'reason': hand_config.yaku.chiihou.name}
            in result['han_details'])
        self.assertEqual(result['han'], 13)

        hand_config = HandConfig(is_tsumo=True,
                                 is_tenhou=True,
                                 is_chiihou=False)
        result = HandCalculator.calculate_hand_score(
            tiles, win_tile, hand_config=hand_config)
        self.assertEqual(len(result['han_details']), 2)
        self.assertTrue(
            {'han': 13, 'reason': hand_config.yaku.kokushi_musou.name}
            in result['han_details'])
        self.assertFalse(
            {'han': 26, 'reason': hand_config.yaku.kokushi_musou_13_men.name}
            in result['han_details'])
        self.assertTrue(
            {'han': 13, 'reason': hand_config.yaku.tenhou.name}
            in result['han_details'])
        self.assertFalse(
            {'han': 13, 'reason': hand_config.yaku.chiihou.name}
            in result['han_details'])
        self.assertEqual(result['han'], 26)

        hand_config = HandConfig(is_tsumo=True,
                                 is_tenhou=False,
                                 is_chiihou=True)
        result = HandCalculator.calculate_hand_score(
            tiles, win_tile, hand_config=hand_config)
        self.assertEqual(len(result['han_details']), 2)
        self.assertTrue(
            {'han': 13, 'reason': hand_config.yaku.kokushi_musou.name}
            in result['han_details'])
        self.assertFalse(
            {'han': 26, 'reason': hand_config.yaku.kokushi_musou_13_men.name}
            in result['han_details'])
        self.assertFalse(
            {'han': 13, 'reason': hand_config.yaku.tenhou.name}
            in result['han_details'])
        self.assertTrue(
            {'han': 13, 'reason': hand_config.yaku.chiihou.name}
            in result['han_details'])
        self.assertEqual(result['han'], 26)

        # kokushi musou 13-men tests

        tiles = Tiles.string_to_array(sou="19", pin="19", man="19",
                                      honours="1234567")
        win_tile = self.__string_to_tile_index(honours="7")
        hand_config = HandConfig(is_tsumo=False,
                                 is_tenhou=False,
                                 is_chiihou=False)
        result = HandCalculator.calculate_hand_score(
            tiles, win_tile, hand_config=hand_config)
        self.assertEqual(len(result['han_details']), 1)
        self.assertFalse(
            {'han': 13, 'reason': hand_config.yaku.kokushi_musou.name}
            in result['han_details'])
        self.assertTrue(
            {'han': 26, 'reason': hand_config.yaku.kokushi_musou_13_men.name}
            in result['han_details'])
        self.assertFalse(
            {'han': 13, 'reason': hand_config.yaku.tenhou.name}
            in result['han_details'])
        self.assertFalse(
            {'han': 13, 'reason': hand_config.yaku.chiihou.name}
            in result['han_details'])
        self.assertEqual(result['han'], 26)

        hand_config = HandConfig(is_tsumo=True,
                                 is_tenhou=True,
                                 is_chiihou=False)
        result = HandCalculator.calculate_hand_score(
            tiles, win_tile, hand_config=hand_config)
        self.assertEqual(len(result['han_details']), 2)
        self.assertFalse(
            {'han': 13, 'reason': hand_config.yaku.kokushi_musou.name}
            in result['han_details'])
        self.assertTrue(
            {'han': 26, 'reason': hand_config.yaku.kokushi_musou_13_men.name}
            in result['han_details'])
        self.assertTrue(
            {'han': 13, 'reason': hand_config.yaku.tenhou.name}
            in result['han_details'])
        self.assertFalse(
            {'han': 13, 'reason': hand_config.yaku.chiihou.name}
            in result['han_details'])
        self.assertEqual(result['han'], 39)

        hand_config = HandConfig(is_tsumo=True,
                                 is_tenhou=False,
                                 is_chiihou=True)
        result = HandCalculator.calculate_hand_score(
            tiles, win_tile, hand_config=hand_config)
        self.assertEqual(len(result['han_details']), 2)
        self.assertFalse(
            {'han': 13, 'reason': hand_config.yaku.kokushi_musou.name}
            in result['han_details'])
        self.assertTrue(
            {'han': 26, 'reason': hand_config.yaku.kokushi_musou_13_men.name}
            in result['han_details'])
        self.assertFalse(
            {'han': 13, 'reason': hand_config.yaku.tenhou.name}
            in result['han_details'])
        self.assertTrue(
            {'han': 13, 'reason': hand_config.yaku.chiihou.name}
            in result['han_details'])
        self.assertEqual(result['han'], 39)


if __name__ == '__main__':
    unittest.main()
