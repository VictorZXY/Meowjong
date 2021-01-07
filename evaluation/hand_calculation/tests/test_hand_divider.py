import unittest

from evaluation.hand_calculation import tile_constants
from evaluation.hand_calculation.hand_divider import HandDivider
from evaluation.hand_calculation.meld import Meld
from evaluation.hand_calculation.tiles import Tiles


class HandDividerTestCase(unittest.TestCase):
    def test_tanyao_division(self):
        hand_divider = HandDivider()
        tiles = Tiles.string_to_array(man='234567', sou='23455', honours='777')
        result = hand_divider.divide_hand(tiles)
        self.assertEqual(len(result), 1)
        self.assertEqual(
            [Tiles.array_to_one_line_string(item) for item in result[0]],
            ['234m', '567m', '234s', '55s', '777z']
        )

    def test_tanyao_division_2(self):
        hand_divider = HandDivider()
        tiles = Tiles.string_to_array(man='123', pin='123', sou='123',
                                      honours='11222')
        result = hand_divider.divide_hand(tiles)
        self.assertEqual(len(result), 1)
        self.assertEqual(
            [Tiles.array_to_one_line_string(item) for item in result[0]],
            ['123m', '123p', '123s', '11z', '222z']
        )

    def test_hand_with_multiple_pairs_division(self):
        hand_divider = HandDivider()
        tiles = Tiles.string_to_array(man='23444', pin='344556', sou='333')
        result = hand_divider.divide_hand(tiles)
        self.assertEqual(len(result), 1)
        self.assertEqual(
            [Tiles.array_to_one_line_string(item) for item in result[0]],
            ['234m', '44m', '345p', '456p', '333s']
        )

    def test_chinitsu_division(self):
        hand_divider = HandDivider()
        tiles = Tiles.string_to_array(man='11122233388899')
        result = hand_divider.divide_hand(tiles)
        self.assertEqual(len(result), 2)
        self.assertEqual(
            [Tiles.array_to_one_line_string(item) for item in result[0]],
            ['111m', '222m', '333m', '888m', '99m']
        )
        self.assertEqual(
            [Tiles.array_to_one_line_string(item) for item in result[1]],
            ['123m', '123m', '123m', '888m', '99m']
        )

    def test_honitsu_division(self):
        hand_divider = HandDivider()
        tiles = Tiles.string_to_array(sou='111123666789', honours='11')
        result = hand_divider.divide_hand(tiles)
        self.assertEqual(len(result), 1)
        self.assertEqual(
            [Tiles.array_to_one_line_string(item) for item in result[0]],
            ['111s', '123s', '666s', '789s', '11z']
        )

    def test_honitsu_with_melds_division(self):
        hand_divider = HandDivider()
        private_tiles = Tiles.string_to_array(pin='778899', honours='22')
        melds = [
            Meld(Meld.CHII, tiles='789p'),
            Meld(Meld.CHII, tiles='234p')
        ]
        result = hand_divider.divide_hand(private_tiles, melds=melds)
        self.assertEqual(len(result), 1)
        self.assertEqual(
            [Tiles.array_to_one_line_string(item) for item in result[0]],
            ['234p', '789p', '789p', '789p', '22z']
        )

    def test_chiitoitsu_like_hand_division(self):
        hand_divider = HandDivider()
        tiles = Tiles.string_to_array(man='112233', pin='99', sou='445566')
        result = hand_divider.divide_hand(tiles)
        self.assertEqual(len(result), 2)
        self.assertEqual(
            [Tiles.array_to_one_line_string(item) for item in result[0]],
            ['11m', '22m', '33m', '99p', '44s', '55s', '66s']
        )
        self.assertEqual(
            [Tiles.array_to_one_line_string(item) for item in result[1]],
            ['123m', '123m', '99p', '456s', '456s']
        )

    def test_hand_with_kan_and_kita_division(self):
        hand_divider = HandDivider()
        private_tiles = Tiles.string_to_array(man='55', honours='222')
        melds = [
            Meld(Meld.KAN, tiles='6666m', is_open=False),
            Meld(Meld.PON, tiles='111p'),
            Meld(Meld.KITA, tiles='4z'),
            Meld(Meld.PON, tiles='777m'),
            Meld(Meld.KITA, tiles='444z')
        ]
        result = hand_divider.divide_hand(private_tiles, melds=melds)
        self.assertEqual(len(result), 1)
        self.assertEqual(
            [Tiles.array_to_one_line_string(item) for item in result[0]],
            ['55m', '6666m', '777m', '111p', '222z']
        )

    def test_hand_with_dora_division(self):
        hand_divider = HandDivider()
        private_tiles = Tiles.string_to_array(man='50', sou='055')
        melds = [
            Meld(Meld.KAN, tiles='6666m', is_open=False),
            Meld(Meld.CHII, tiles='406p'),
            Meld(Meld.KITA, tiles='4z'),
            Meld(Meld.PON, tiles='777m'),
            Meld(Meld.KITA, tiles='444z')
        ]
        result = hand_divider.divide_hand(private_tiles, melds=melds)
        self.assertEqual(len(result), 1)
        self.assertEqual(
            [Tiles.array_to_one_line_string(item) for item in result[0]],
            ['55m', '6666m', '777m', '456p', '555s']
        )

    def test_kokushi_musou_division(self):
        hand_divider = HandDivider()
        private_tiles = Tiles.one_line_string_to_array('19m19p19s12345677z')
        result = hand_divider.divide_hand(private_tiles)
        self.assertEqual(len(result), 34)
        self.assertEqual(
            Tiles.array_to_one_line_string(result),
            '19m19p19s12345677z'
        )

    def test_incomplete_hand_division(self):
        hand_divider = HandDivider()
        private_tiles = Tiles.string_to_array(man='147', pin='258', sou='369',
                                              honours='1234')
        result = hand_divider.divide_hand(private_tiles)
        self.assertEqual(len(result), 34)
        self.assertEqual(
            Tiles.array_to_one_line_string(result),
            '147m258p369s1234z'
        )

    def test_hand_division_miscellaneous(self):
        tiles = Tiles.string_to_array(pin='99', honours='77')
        win_tile = tile_constants.NINE_PIN
        melds = [
            Meld(Meld.PON, tiles='111z'),
            Meld(Meld.CHII, tiles='123p'),
            Meld(Meld.CHII, tiles='123p'),
        ]

        result = HandDivider.divide_hand(tiles, win_tile, melds)
        self.assertEqual(len(result), 1)
        self.assertEqual(
            [Tiles.array_to_one_line_string(item) for item in result[0]],
            ['123p', '123p', '999p', '111z', '77z']
        )


if __name__ == '__main__':
    unittest.main()
