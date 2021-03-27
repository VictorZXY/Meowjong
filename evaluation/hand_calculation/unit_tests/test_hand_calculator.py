import unittest

from evaluation.hand_calculation.hand_calculator import HandCalculator, \
    NoYakuError
from evaluation.hand_calculation.hand_config import HandConfig
from evaluation.hand_calculation.hand_divider import HandDivider
from evaluation.hand_calculation.meld import Meld
from evaluation.hand_calculation.tile_constants import ONE_MAN, ONE_PIN, \
    ONE_SOU, EAST, SOUTH, WEST, NORTH, RED_FIVE_MAN, RED_FIVE_PIN, RED_FIVE_SOU
from evaluation.hand_calculation.tiles import Tiles


class HandCalculatorTestCase(unittest.TestCase):
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

    def test_result_miscellaneous(self):
        seat_wind = prevalent_wind = EAST

        tiles = Tiles.string_to_array(pin='99', honours='77')
        win_tile = self.__string_to_tile_index(pin='9')
        melds = [
            self.__make_meld(Meld.PON, honours='111'),
            self.__make_meld(Meld.CHII, pin='123'),
            self.__make_meld(Meld.CHII, pin='123'),
        ]
        result = HandCalculator.calculate_hand_score(
            tiles, win_tile, melds=melds,
            hand_config=HandConfig(seat_wind=seat_wind,
                                   prevalent_wind=prevalent_wind)
        )
        self.assertEqual(result['fu'], 30)

        tiles = Tiles.string_to_array(pin='2244456799')
        win_tile = self.__string_to_tile_index(pin='2')
        dora_indicators = [self.__string_to_tile_index(sou='3'),
                           self.__string_to_tile_index(honours='3')]
        melds = [self.__make_meld(Meld.KAN, honours='4444')]
        result = HandCalculator.calculate_hand_score(
            tiles, win_tile, dora_indicators=dora_indicators, melds=melds,
            hand_config=HandConfig(seat_wind=seat_wind,
                                   prevalent_wind=prevalent_wind)
        )
        self.assertEqual(result['han'], 6)
        self.assertEqual(result['fu'], 50)
        self.assertEqual(len(result['han_details']), 2)

        tiles = Tiles.string_to_array(sou='678', man='11', pin='12345',
                                      honours='666')
        win_tile = self.__string_to_tile_index(pin='3')
        result = HandCalculator.calculate_hand_score(
            tiles, win_tile,
            hand_config=HandConfig(seat_wind=seat_wind,
                                   prevalent_wind=prevalent_wind,
                                   is_tsumo=True)
        )
        self.assertEqual(result['fu'], 40)

        tiles = Tiles.string_to_array(man='234789', pin='1234566')
        win_tile = self.__string_to_tile_index(pin='6')
        result = HandCalculator.calculate_hand_score(
            tiles, win_tile,
            hand_config=HandConfig(seat_wind=seat_wind,
                                   prevalent_wind=prevalent_wind)
        )
        self.assertEqual(result['fu'], 30)

        tiles = Tiles.string_to_array(sou='678', pin='3455789', honours='555')
        win_tile = self.__string_to_tile_index(pin='5')
        result = HandCalculator.calculate_hand_score(
            tiles, win_tile,
            hand_config=HandConfig(seat_wind=seat_wind,
                                   prevalent_wind=prevalent_wind,
                                   is_tsumo=True)
        )
        self.assertEqual(result['fu'], 40)

        tiles = Tiles.string_to_array(sou='12345678', man='678', pin='88')
        win_tile = self.__string_to_tile_index(sou='3')
        result = HandCalculator.calculate_hand_score(
            tiles, win_tile,
            hand_config=HandConfig(seat_wind=seat_wind,
                                   prevalent_wind=prevalent_wind)
        )
        self.assertEqual(result['han'], 1)
        self.assertEqual(result['fu'], 30)
        self.assertEqual(len(result['han_details']), 1)

        tiles = Tiles.string_to_array(sou='2399', man='123456', pin='456')
        win_tile = self.__string_to_tile_index(sou='1')
        result = HandCalculator.calculate_hand_score(
            tiles, win_tile,
            hand_config=HandConfig(seat_wind=seat_wind,
                                   prevalent_wind=prevalent_wind)
        )
        self.assertEqual(result['han'], 1)
        self.assertEqual(result['fu'], 30)
        self.assertEqual(len(result['han_details']), 1)

        tiles = Tiles.string_to_array(sou='11123789', honours='11')
        win_tile = self.__string_to_tile_index(sou='1')
        melds = [self.__make_meld(Meld.PON, sou='666')]
        dora_indicators = [self.__string_to_tile_index(honours='4')]
        result = HandCalculator.calculate_hand_score(
            tiles,
            win_tile,
            melds=melds,
            dora_indicators=dora_indicators,
            hand_config=HandConfig(seat_wind=seat_wind,
                                   prevalent_wind=prevalent_wind)
        )
        self.assertEqual(result['fu'], 40)
        self.assertEqual(result['han'], 4)

        tiles = Tiles.string_to_array(pin='1233', sou='567')
        win_tile = self.__string_to_tile_index(pin='3')
        melds = [self.__make_meld(Meld.PON, honours='666'),
                 self.__make_meld(Meld.PON, honours='777')]
        result = HandCalculator.calculate_hand_score(
            tiles, win_tile, melds=melds,
            hand_config=HandConfig(seat_wind=seat_wind,
                                   prevalent_wind=prevalent_wind)
        )
        self.assertEqual(result['fu'], 30)
        self.assertEqual(result['han'], 2)

        tiles = Tiles.string_to_array(pin='1236778', sou='678', man='456')
        win_tile = self.__string_to_tile_index(pin='7')
        result = HandCalculator.calculate_hand_score(
            tiles, win_tile,
            hand_config=HandConfig(seat_wind=seat_wind,
                                   prevalent_wind=prevalent_wind,
                                   is_riichi=True)
        )
        self.assertEqual(result['fu'], 40)
        self.assertEqual(result['han'], 1)

        tiles = Tiles.string_to_array(man='5699')
        win_tile = self.__string_to_tile_index(man='7')
        melds = [
            self.__make_meld(Meld.KAN, honours='7777'),
            self.__make_meld(Meld.PON, man='111'),
            self.__make_meld(Meld.CHII, man='678'),

        ]
        result = HandCalculator.calculate_hand_score(
            tiles, win_tile, melds=melds,
            hand_config=HandConfig(seat_wind=seat_wind,
                                   prevalent_wind=prevalent_wind)
        )
        self.assertEqual(result['fu'], 40)
        self.assertEqual(result['han'], 3)

        tiles = Tiles.string_to_array(man='22888', honours='66')
        win_tile = self.__string_to_tile_index(man='2')
        melds = [self.__make_meld(Meld.CHII, man='123'),
                 self.__make_meld(Meld.PON, man='777')]
        result = HandCalculator.calculate_hand_score(
            tiles, win_tile, melds=melds,
            hand_config=HandConfig(seat_wind=seat_wind,
                                   prevalent_wind=prevalent_wind)
        )
        self.assertEqual(result['fu'], 30)
        self.assertEqual(result['han'], 2)

        tiles = Tiles.string_to_array(pin='4467')
        win_tile = self.__string_to_tile_index(pin='8')
        melds = [
            self.__make_meld(Meld.PON, honours='444'),
            self.__make_meld(Meld.PON, pin='111'),
            self.__make_meld(Meld.PON, pin='888'),
        ]
        result = HandCalculator.calculate_hand_score(
            tiles, win_tile, melds=melds,
            hand_config=HandConfig(seat_wind=seat_wind,
                                   prevalent_wind=prevalent_wind)
        )
        self.assertEqual(result['fu'], 30)
        self.assertEqual(result['han'], 2)

        tiles = Tiles.string_to_array(sou='6778', man='345', pin='999',
                                      honours='222')
        win_tile = self.__string_to_tile_index(sou='7')
        result = HandCalculator.calculate_hand_score(
            tiles, win_tile,
            hand_config=HandConfig(seat_wind=seat_wind,
                                   prevalent_wind=prevalent_wind,
                                   is_tsumo=True)
        )
        self.assertEqual(result['fu'], 40)
        self.assertEqual(result['han'], 1)

        tiles = Tiles.string_to_array(sou='3344557789', man='345')
        win_tile = self.__string_to_tile_index(sou='7')
        result = HandCalculator.calculate_hand_score(
            tiles, win_tile,
            hand_config=HandConfig(seat_wind=seat_wind,
                                   prevalent_wind=prevalent_wind,
                                   is_tsumo=True)
        )
        self.assertEqual(result['fu'], 30)
        self.assertEqual(result['han'], 2)

        tiles = Tiles.string_to_array(pin='12667788', honours='22')
        win_tile = self.__string_to_tile_index(pin='3')
        melds = [self.__make_meld(Meld.CHII, pin='123')]
        result = HandCalculator.calculate_hand_score(
            tiles, win_tile, melds=melds,
            hand_config=HandConfig(seat_wind=seat_wind,
                                   prevalent_wind=prevalent_wind)
        )
        self.assertEqual(result['fu'], 30)
        self.assertEqual(result['han'], 2)

        tiles = Tiles.string_to_array(sou='345', man='1233456789')
        win_tile = self.__string_to_tile_index(man='3')
        result = HandCalculator.calculate_hand_score(
            tiles, win_tile,
            hand_config=HandConfig(seat_wind=seat_wind,
                                   prevalent_wind=prevalent_wind)
        )
        self.assertEqual(result['fu'], 40)
        self.assertEqual(result['han'], 2)

        tiles = Tiles.string_to_array(sou='1156')
        melds = [
            self.__make_meld(Meld.CHII, sou='123'),
            self.__make_meld(Meld.PON, sou='777'),
            self.__make_meld(Meld.PON, sou='888'),
        ]
        win_tile = self.__string_to_tile_index(sou='4')
        result = HandCalculator.calculate_hand_score(
            tiles, win_tile, melds=melds,
            hand_config=HandConfig(seat_wind=seat_wind,
                                   prevalent_wind=prevalent_wind,
                                   is_tsumo=True)
        )
        self.assertEqual(result['fu'], 30)
        self.assertEqual(result['han'], 5)

        tiles = Tiles.string_to_array(sou='13789', honours='55777')
        melds = [self.__make_meld(Meld.CHII, sou='123')]
        win_tile = self.__string_to_tile_index(sou='2')
        result = HandCalculator.calculate_hand_score(
            tiles, win_tile, melds=melds,
            hand_config=HandConfig(seat_wind=seat_wind,
                                   prevalent_wind=prevalent_wind)
        )
        self.assertEqual(result['fu'], 40)
        self.assertEqual(result['han'], 4)

        tiles = Tiles.string_to_array(pin='77889', honours='22')
        melds = [self.__make_meld(Meld.CHII, pin='234'),
                 self.__make_meld(Meld.CHII, pin='789')]
        win_tile = self.__string_to_tile_index(pin='9')
        result = HandCalculator.calculate_hand_score(
            tiles, win_tile, melds=melds,
            hand_config=HandConfig(seat_wind=seat_wind,
                                   prevalent_wind=prevalent_wind)
        )
        self.assertEqual(result['fu'], 30)
        self.assertEqual(result['han'], 2)

        tiles = Tiles.string_to_array(pin='7788899')
        melds = [self.__make_meld(Meld.PON, honours='777'),
                 self.__make_meld(Meld.PON, man='444')]
        win_tile = self.__string_to_tile_index(pin='8')
        result = HandCalculator.calculate_hand_score(
            tiles, win_tile, melds=melds,
            hand_config=HandConfig(seat_wind=seat_wind,
                                   prevalent_wind=prevalent_wind,
                                   is_tsumo=True)
        )
        self.assertEqual(result['fu'], 30)
        self.assertEqual(result['han'], 1)

        tiles = Tiles.string_to_array(pin='1233345', honours='555', man='567')
        win_tile = self.__string_to_tile_index(pin='3')
        result = HandCalculator.calculate_hand_score(
            tiles, win_tile,
            hand_config=HandConfig(seat_wind=seat_wind,
                                   prevalent_wind=prevalent_wind)
        )
        self.assertEqual(result['fu'], 40)
        self.assertEqual(result['han'], 1)

        tiles = Tiles.string_to_array(pin='6777889', honours='555')
        win_tile = self.__string_to_tile_index(pin='7')
        melds = [self.__make_meld(Meld.CHII, pin='345')]
        result = HandCalculator.calculate_hand_score(
            tiles, win_tile, melds=melds,
            hand_config=HandConfig(seat_wind=seat_wind,
                                   prevalent_wind=prevalent_wind)
        )
        self.assertEqual(result['fu'], 30)
        self.assertEqual(result['han'], 3)

        tiles = Tiles.string_to_array(pin='567', sou='33555', honours='77')
        win_tile = self.__string_to_tile_index(sou='3')
        melds = [self.__make_meld(Meld.KAN, is_open=False, sou='4444')]
        result = HandCalculator.calculate_hand_score(
            tiles, win_tile, melds=melds,
            hand_config=HandConfig(seat_wind=seat_wind,
                                   prevalent_wind=prevalent_wind,
                                   is_riichi=True)
        )
        self.assertEqual(result['fu'], 60)
        self.assertEqual(result['han'], 1)

        tiles = Tiles.string_to_array(man='5', honours='222')
        win_tile = self.__string_to_tile_index(man='4')
        melds = [
            self.__make_meld(Meld.PON, pin='111'),
            self.__make_meld(Meld.KAN, man='6666', is_open=False),
            self.__make_meld(Meld.PON, man='777'),
        ]
        self.assertRaises(
            NoYakuError,
            HandCalculator.calculate_hand_score, tiles, win_tile, melds
        )

    def test_menzen_tsumo(self):
        tiles = Tiles.string_to_array(sou='12344', man='234456', pin='66')
        win_tile = self.__string_to_tile_index(sou='4')
        result = HandCalculator.calculate_hand_score(
            tiles, win_tile,
            hand_config=HandConfig(is_menzen=True, is_tsumo=True))
        self.assertEqual(result['han'], 1)
        self.assertEqual(result['fu'], 30)
        self.assertEqual(len(result['han_details']), 1)

    def test_riichi(self):
        tiles = Tiles.string_to_array(sou='12344', man='234456', pin='66')
        win_tile = self.__string_to_tile_index(sou='4')
        result = HandCalculator.calculate_hand_score(
            tiles, win_tile, hand_config=HandConfig(is_riichi=True))
        self.assertEqual(result['han'], 1)
        self.assertEqual(result['fu'], 40)
        self.assertEqual(len(result['han_details']), 1)

    def test_ippatsu(self):
        tiles = Tiles.string_to_array(sou='12344', man='234456', pin='66')
        win_tile = self.__string_to_tile_index(sou='4')
        result = HandCalculator.calculate_hand_score(
            tiles, win_tile,
            hand_config=HandConfig(is_riichi=True, is_ippatsu=True))
        self.assertEqual(result['han'], 2)
        self.assertEqual(result['fu'], 40)
        self.assertEqual(len(result['han_details']), 2)

    def test_chankan(self):
        tiles = Tiles.string_to_array(sou='12344', man='234456', pin='66')
        win_tile = self.__string_to_tile_index(sou='4')
        result = HandCalculator.calculate_hand_score(
            tiles, win_tile, hand_config=HandConfig(is_chankan=True))
        self.assertEqual(result['han'], 1)
        self.assertEqual(result['fu'], 40)
        self.assertEqual(len(result['han_details']), 1)

    def test_rinshan(self):
        tiles = Tiles.string_to_array(sou='12344', man='234456', pin='66')
        win_tile = self.__string_to_tile_index(sou='4')
        result = HandCalculator.calculate_hand_score(
            tiles, win_tile, hand_config=HandConfig(is_rinshan=True))
        self.assertEqual(result['han'], 1)
        self.assertEqual(result['fu'], 40)
        self.assertEqual(len(result['han_details']), 1)

    def test_haitei(self):
        tiles = Tiles.string_to_array(sou='12344', man='234456', pin='66')
        win_tile = self.__string_to_tile_index(sou='4')
        result = HandCalculator.calculate_hand_score(
            tiles, win_tile, hand_config=HandConfig(is_haitei=True))
        self.assertEqual(result['han'], 1)
        self.assertEqual(result['fu'], 40)
        self.assertEqual(len(result['han_details']), 1)

    def test_houtei(self):
        tiles = Tiles.string_to_array(sou='12344', man='234456', pin='66')
        win_tile = self.__string_to_tile_index(sou='4')
        result = HandCalculator.calculate_hand_score(
            tiles, win_tile, hand_config=HandConfig(is_houtei=True))
        self.assertEqual(result['han'], 1)
        self.assertEqual(result['fu'], 40)
        self.assertEqual(len(result['han_details']), 1)

    def test_east(self):
        seat_wind, prevalent_wind = EAST, WEST

        tiles = Tiles.string_to_array(sou='234567', man='23422', honours='11')
        win_tile = self.__string_to_tile_index(honours='1')
        result = HandCalculator.calculate_hand_score(
            tiles,
            win_tile,
            hand_config=HandConfig(
                is_tsumo=False, is_riichi=False, seat_wind=seat_wind,
                prevalent_wind=prevalent_wind
            )
        )
        self.assertEqual(result['han'], 1)
        self.assertEqual(result['fu'], 40)
        self.assertEqual(len(result['han_details']), 1)

        prevalent_wind = EAST
        result = HandCalculator.calculate_hand_score(
            tiles,
            win_tile,
            hand_config=HandConfig(
                is_tsumo=False, is_riichi=False, seat_wind=seat_wind,
                prevalent_wind=prevalent_wind
            ),
        )
        self.assertEqual(result['han'], 2)
        self.assertEqual(result['fu'], 40)
        self.assertEqual(len(result['han_details']), 2)

    def test_south(self):
        seat_wind, prevalent_wind = SOUTH, EAST

        tiles = Tiles.string_to_array(sou='234567', man='23422', honours='22')
        win_tile = self.__string_to_tile_index(honours='2')
        result = HandCalculator.calculate_hand_score(
            tiles,
            win_tile,
            hand_config=HandConfig(
                is_tsumo=False, is_riichi=False, seat_wind=seat_wind,
                prevalent_wind=prevalent_wind
            ),
        )
        self.assertEqual(result['han'], 1)
        self.assertEqual(result['fu'], 40)
        self.assertEqual(len(result['han_details']), 1)

        prevalent_wind = SOUTH
        result = HandCalculator.calculate_hand_score(
            tiles,
            win_tile,
            hand_config=HandConfig(
                is_tsumo=False, is_riichi=False, seat_wind=seat_wind,
                prevalent_wind=prevalent_wind
            ),
        )
        self.assertEqual(result['han'], 2)
        self.assertEqual(result['fu'], 40)
        self.assertEqual(len(result['han_details']), 2)

    def test_west(self):
        seat_wind, prevalent_wind = WEST, EAST

        tiles = Tiles.string_to_array(sou='234567', man='23422', honours='33')
        win_tile = self.__string_to_tile_index(honours='3')
        result = HandCalculator.calculate_hand_score(
            tiles,
            win_tile,
            hand_config=HandConfig(
                is_tsumo=False, is_riichi=False, seat_wind=seat_wind,
                prevalent_wind=prevalent_wind
            ),
        )
        self.assertEqual(result['han'], 1)
        self.assertEqual(result['fu'], 40)
        self.assertEqual(len(result['han_details']), 1)

        prevalent_wind = WEST
        result = HandCalculator.calculate_hand_score(
            tiles,
            win_tile,
            hand_config=HandConfig(
                is_tsumo=False, is_riichi=False, seat_wind=seat_wind,
                prevalent_wind=prevalent_wind
            ),
        )
        self.assertEqual(result['han'], 2)
        self.assertEqual(result['fu'], 40)
        self.assertEqual(len(result['han_details']), 2)

    def test_north(self):
        seat_wind, prevalent_wind = NORTH, EAST

        tiles = Tiles.string_to_array(sou='234567', man='23422', honours='44')
        win_tile = self.__string_to_tile_index(honours='4')
        result = HandCalculator.calculate_hand_score(
            tiles,
            win_tile,
            hand_config=HandConfig(
                is_tsumo=False, is_riichi=False, seat_wind=seat_wind,
                prevalent_wind=prevalent_wind
            ),
        )
        self.assertEqual(result['han'], 1)
        self.assertEqual(result['fu'], 40)
        self.assertEqual(len(result['han_details']), 1)

        prevalent_wind = NORTH
        result = HandCalculator.calculate_hand_score(
            tiles,
            win_tile,
            hand_config=HandConfig(
                is_tsumo=False, is_riichi=False, seat_wind=seat_wind,
                prevalent_wind=prevalent_wind
            ),
        )
        self.assertEqual(result['han'], 2)
        self.assertEqual(result['fu'], 40)
        self.assertEqual(len(result['han_details']), 2)

    def test_haku(self):
        tiles = Tiles.string_to_array(sou='234567', man='23422', honours='55')
        win_tile = self.__string_to_tile_index(honours='5')
        result = HandCalculator.calculate_hand_score(
            tiles, win_tile,
            hand_config=HandConfig(is_tsumo=False, is_riichi=False)
        )
        self.assertEqual(result['han'], 1)
        self.assertEqual(result['fu'], 40)
        self.assertEqual(len(result['han_details']), 1)

    def test_hatsu(self):
        tiles = Tiles.string_to_array(sou='234567', man='23422', honours='66')
        win_tile = self.__string_to_tile_index(honours='6')
        result = HandCalculator.calculate_hand_score(
            tiles, win_tile,
            hand_config=HandConfig(is_tsumo=False, is_riichi=False)
        )
        self.assertEqual(result['han'], 1)
        self.assertEqual(result['fu'], 40)
        self.assertEqual(len(result['han_details']), 1)

    def test_chun(self):
        tiles = Tiles.string_to_array(sou='234567', man='23422', honours='77')
        win_tile = self.__string_to_tile_index(honours='7')
        result = HandCalculator.calculate_hand_score(
            tiles, win_tile,
            hand_config=HandConfig(is_tsumo=False, is_riichi=False)
        )
        self.assertEqual(result['han'], 1)
        self.assertEqual(result['fu'], 40)
        self.assertEqual(len(result['han_details']), 1)

    def test_tanyao(self):
        tiles = Tiles.string_to_array(sou='234567', man='23456', pin='22')
        win_tile = self.__string_to_tile_index(man='7')
        result = HandCalculator.calculate_hand_score(
            tiles, win_tile,
            hand_config=HandConfig(is_tsumo=False, is_riichi=True)
        )
        self.assertEqual(result['han'], 3)
        self.assertEqual(result['fu'], 30)
        self.assertEqual(len(result['han_details']), 3)

        tiles = Tiles.string_to_array(sou='567', man='23456', pin='22')
        win_tile = self.__string_to_tile_index(man='7')
        melds = [self.__make_meld(Meld.CHII, sou='234')]
        result = HandCalculator.calculate_hand_score(
            tiles, win_tile, melds=melds,
            hand_config=HandConfig()
        )
        self.assertEqual(result['han'], 1)
        self.assertEqual(result['fu'], 30)
        self.assertEqual(len(result['han_details']), 1)

    def test_iipeiko(self):
        tiles = Tiles.string_to_array(sou='112233', man='33', pin='12344')
        win_tile = self.__string_to_tile_index(man='3')
        result = HandCalculator.calculate_hand_score(tiles, win_tile)
        self.assertEqual(result['han'], 1)
        self.assertEqual(result['fu'], 40)
        self.assertEqual(len(result['han_details']), 1)

        tiles = Tiles.string_to_array(sou='123', man='33', pin='12344')
        melds = [self.__make_meld(Meld.CHII, sou='123')]
        self.assertRaises(
            NoYakuError,
            HandCalculator.calculate_hand_score, tiles, win_tile, melds=melds
        )

        tiles = Tiles.string_to_array(sou='112233', man='33', pin='44')
        melds = [self.__make_meld(Meld.CHII, pin='123')]
        self.assertRaises(
            NoYakuError,
            HandCalculator.calculate_hand_score, tiles, win_tile, melds=melds
        )

    def test_pinfu(self):
        seat_wind, prevalent_wind = EAST, WEST

        tiles = Tiles.string_to_array(sou='123456', man='12345', pin='55')
        win_tile = self.__string_to_tile_index(man='6')
        result = HandCalculator.calculate_hand_score(
            tiles, win_tile,
            hand_config=HandConfig(seat_wind=seat_wind,
                                   prevalent_wind=prevalent_wind)
        )
        self.assertEqual(result['han'], 1)
        self.assertEqual(result['fu'], 30)
        self.assertEqual(len(result['han_details']), 1)

        # waiting in two pairs
        tiles = Tiles.string_to_array(sou='123456', man='12355', pin='55')
        win_tile = self.__string_to_tile_index(man='5')
        self.assertRaises(NoYakuError,
                          HandCalculator.calculate_hand_score, tiles, win_tile)

        # contains pon or kan
        tiles = Tiles.string_to_array(sou='111456', man='12345', pin='55')
        win_tile = self.__string_to_tile_index(man='6')
        self.assertRaises(NoYakuError,
                          HandCalculator.calculate_hand_score, tiles, win_tile)

        # edge wait
        tiles = Tiles.string_to_array(sou='12456', man='123456', pin='55')
        win_tile = self.__string_to_tile_index(sou='3')
        self.assertRaises(NoYakuError,
                          HandCalculator.calculate_hand_score, tiles, win_tile)

        # closed wait
        tiles = Tiles.string_to_array(sou='12357', man='123456', pin='55')
        win_tile = self.__string_to_tile_index(sou='6')
        self.assertRaises(NoYakuError,
                          HandCalculator.calculate_hand_score, tiles, win_tile)

        # pair wait
        tiles = Tiles.string_to_array(man='2456678', pin='123678')
        win_tile = self.__string_to_tile_index(man='2')
        self.assertRaises(NoYakuError,
                          HandCalculator.calculate_hand_score, tiles, win_tile)

        # valued pair
        tiles = Tiles.string_to_array(sou='12378', man='123456', honours='11')
        win_tile = self.__string_to_tile_index(sou='6')
        self.assertRaises(
            NoYakuError,
            HandCalculator.calculate_hand_score, tiles, win_tile,
            hand_config=HandConfig(seat_wind=seat_wind,
                                   prevalent_wind=prevalent_wind)
        )

        # not valued pair
        tiles = Tiles.string_to_array(sou='12378', man='123456', honours='22')
        win_tile = self.__string_to_tile_index(sou='6')
        result = HandCalculator.calculate_hand_score(tiles, win_tile)
        self.assertEqual(result['han'], 1)
        self.assertEqual(result['fu'], 30)
        self.assertEqual(len(result['han_details']), 1)

        # open hand
        tiles = Tiles.string_to_array(sou='99', man='23456', pin='456')
        win_tile = self.__string_to_tile_index(man='1')
        melds = [self.__make_meld(Meld.CHII, sou='123')]
        self.assertRaises(
            NoYakuError,
            HandCalculator.calculate_hand_score, tiles, win_tile, melds=melds
        )

    def test_chanta(self):
        tiles = Tiles.string_to_array(sou='123', man='123789', honours='2233')
        win_tile = self.__string_to_tile_index(honours='3')
        result = HandCalculator.calculate_hand_score(tiles, win_tile)
        self.assertEqual(result['han'], 2)
        self.assertEqual(result['fu'], 40)
        self.assertEqual(len(result['han_details']), 1)

        tiles = Tiles.string_to_array(man='123789', honours='2233')
        melds = [self.__make_meld(Meld.CHII, sou='123')]
        result = HandCalculator.calculate_hand_score(
            tiles, win_tile, melds=melds)
        self.assertEqual(result['han'], 1)
        self.assertEqual(result['fu'], 30)
        self.assertEqual(len(result['han_details']), 1)

    def test_ikkitsuukan(self):
        hand_config = HandConfig()

        tiles = Tiles.string_to_array(man='123456789', sou='123', honours='22')
        self.assertTrue(hand_config.yaku.ikkitsuukan.is_condition_met(
            HandDivider.divide_hand(tiles)[0]))

        tiles = Tiles.string_to_array(man='112233456789', honours='22')
        self.assertTrue(hand_config.yaku.ikkitsuukan.is_condition_met(
            HandDivider.divide_hand(tiles)[0]))

        tiles = Tiles.string_to_array(man='122334567789', honours='11')
        self.assertFalse(hand_config.yaku.ikkitsuukan.is_condition_met(
            HandDivider.divide_hand(tiles)[0]))

        tiles = Tiles.string_to_array(man='123456789', sou='12', honours='22')
        win_tile = self.__string_to_tile_index(sou='3')
        result = HandCalculator.calculate_hand_score(tiles, win_tile)
        self.assertEqual(result['han'], 2)
        self.assertEqual(result['fu'], 40)
        self.assertEqual(len(result['han_details']), 1)

        tiles = Tiles.string_to_array(man='456789', sou='12', honours='22')
        melds = [self.__make_meld(Meld.CHII, man='123')]
        result = HandCalculator.calculate_hand_score(
            tiles, win_tile, melds=melds)
        self.assertEqual(result['han'], 1)
        self.assertEqual(result['fu'], 30)
        self.assertEqual(len(result['han_details']), 1)

    def test_sanshoku_doujun(self):
        tiles = Tiles.string_to_array(sou='123456', man='1399', pin='123')
        win_tile = self.__string_to_tile_index(man='2')
        result = HandCalculator.calculate_hand_score(tiles, win_tile)
        self.assertEqual(result['han'], 2)
        self.assertEqual(result['fu'], 40)
        self.assertEqual(len(result['han_details']), 1)

        tiles = Tiles.string_to_array(sou='456', man='1399', pin='123')
        melds = [self.__make_meld(Meld.CHII, sou='123')]
        result = HandCalculator.calculate_hand_score(
            tiles, win_tile, melds=melds)
        self.assertEqual(result['han'], 1)
        self.assertEqual(result['fu'], 30)
        self.assertEqual(len(result['han_details']), 1)

    def test_sanshoku_doukou(self):
        tiles = Tiles.string_to_array(man='222', pin='2224569')
        melds = [self.__make_meld(Meld.CHII, sou='222')]
        win_tile = self.__string_to_tile_index(pin='9')
        result = HandCalculator.calculate_hand_score(
            tiles, win_tile, melds=melds)
        self.assertEqual(result['han'], 2)
        self.assertEqual(result['fu'], 40)
        self.assertEqual(len(result['han_details']), 1)

    def test_double_riichi(self):
        tiles = Tiles.string_to_array(sou='12344', man='234456', pin='66')
        win_tile = self.__string_to_tile_index(sou='4')
        result = HandCalculator.calculate_hand_score(
            tiles, win_tile,
            hand_config=HandConfig(is_double_riichi=True, is_riichi=True))
        self.assertEqual(result['han'], 2)
        self.assertEqual(result['fu'], 40)
        self.assertEqual(len(result['han_details']), 1)

    def test_toitoi(self):
        tiles = Tiles.string_to_array(man='333', pin='4455')
        melds = [self.__make_meld(Meld.PON, sou='111'),
                 self.__make_meld(Meld.PON, sou='333')]
        win_tile = self.__string_to_tile_index(pin='5')
        result = HandCalculator.calculate_hand_score(
            tiles, win_tile, melds=melds)
        self.assertEqual(result['han'], 2)
        self.assertEqual(result['fu'], 40)
        self.assertEqual(len(result['han_details']), 1)

        tiles = Tiles.string_to_array(pin='77788899', honours='44')
        melds = [self.__make_meld(Meld.PON, sou='777')]
        win_tile = self.__string_to_tile_index(pin='9')
        result = HandCalculator.calculate_hand_score(
            tiles, win_tile, melds=melds)
        self.assertEqual(result['han'], 2)
        self.assertEqual(result['fu'], 40)
        self.assertEqual(len(result['han_details']), 1)

    def test_sankantsu(self):
        tiles = Tiles.string_to_array(man='12', pin='44')
        melds = [
            self.__make_meld(Meld.KAN, sou='1111'),
            self.__make_meld(Meld.KAN, sou='3333'),
            self.__make_meld(Meld.KAN, pin='6666'),
        ]
        win_tile = self.__string_to_tile_index(man='3')
        result = HandCalculator.calculate_hand_score(
            tiles, win_tile, melds=melds)
        self.assertEqual(result['han'], 2)
        self.assertEqual(result['fu'], 60)
        self.assertEqual(len(result['han_details']), 1)

    def test_sanankou(self):
        tiles = Tiles.string_to_array(sou='444', man='333', pin='4455')
        melds = [self.__make_meld(Meld.CHII, sou='123')]
        win_tile = self.__string_to_tile_index(pin='5')
        result = HandCalculator.calculate_hand_score(
            tiles, win_tile, melds=melds, hand_config=HandConfig(is_tsumo=True))
        self.assertEqual(result['han'], 2)
        self.assertEqual(result['fu'], 40)
        self.assertEqual(len(result['han_details']), 1)

    def test_shousangen(self):
        tiles = Tiles.string_to_array(sou='123', man='345', honours='5566677')
        win_tile = self.__string_to_tile_index(honours='7')
        result = HandCalculator.calculate_hand_score(tiles, win_tile)
        self.assertEqual(result['han'], 4)
        self.assertEqual(result['fu'], 50)
        self.assertEqual(len(result['han_details']), 3)

    def test_honroutou(self):
        tiles = Tiles.string_to_array(sou='999', man='111', honours='1122')
        win_tile = self.__string_to_tile_index(honours='2')
        melds = [self.__make_meld(Meld.PON, sou='111')]
        result = HandCalculator.calculate_hand_score(
            tiles, win_tile, melds=melds)
        self.assertEqual(result['han'], 4)
        self.assertEqual(result['fu'], 50)
        self.assertEqual(len(result['han_details']), 2)

        tiles = Tiles.string_to_array(pin='11', honours='22334466', man='199')
        win_tile = self.__string_to_tile_index(man='1')
        result = HandCalculator.calculate_hand_score(tiles, win_tile)
        self.assertEqual(result['fu'], 25)
        self.assertEqual(result['han'], 4)

    def test_chiitoitsu(self):
        tiles = Tiles.string_to_array(sou='113355', man='113355', pin='1')
        win_tile = self.__string_to_tile_index(pin='1')
        result = HandCalculator.calculate_hand_score(tiles, win_tile)
        self.assertEqual(result['han'], 2)
        self.assertEqual(result['fu'], 25)
        self.assertEqual(len(result['han_details']), 1)

    def test_junchan(self):
        tiles = Tiles.string_to_array(sou='789', man='13789', pin='12399')
        win_tile = self.__string_to_tile_index(man='2')
        result = HandCalculator.calculate_hand_score(tiles, win_tile)
        self.assertEqual(result['han'], 3)
        self.assertEqual(result['fu'], 40)
        self.assertEqual(len(result['han_details']), 1)

        tiles = Tiles.string_to_array(man='13789', pin='12399')
        melds = [self.__make_meld(Meld.CHII, sou='789')]
        result = HandCalculator.calculate_hand_score(
            tiles, win_tile, melds=melds)
        self.assertEqual(result['han'], 2)
        self.assertEqual(result['fu'], 30)
        self.assertEqual(len(result['han_details']), 1)

    def test_honitsu(self):
        tiles = Tiles.string_to_array(man='123455667', honours='1112')
        win_tile = self.__string_to_tile_index(honours='2')
        result = HandCalculator.calculate_hand_score(tiles, win_tile)
        self.assertEqual(result['han'], 3)
        self.assertEqual(result['fu'], 40)
        self.assertEqual(len(result['han_details']), 1)

        tiles = Tiles.string_to_array(man='455667', honours='1112')
        melds = [self.__make_meld(Meld.CHII, man='123')]
        result = HandCalculator.calculate_hand_score(
            tiles, win_tile, melds=melds)
        self.assertEqual(result['han'], 2)
        self.assertEqual(result['fu'], 30)
        self.assertEqual(len(result['han_details']), 1)

    def test_ryanpeiko(self):
        tiles = Tiles.string_to_array(sou='112233', man='33', pin='22344')
        win_tile = self.__string_to_tile_index(pin='3')
        result = HandCalculator.calculate_hand_score(tiles, win_tile)
        self.assertEqual(result['han'], 3)
        self.assertEqual(result['fu'], 40)
        self.assertEqual(len(result['han_details']), 1)

        tiles = Tiles.string_to_array(sou='123', man='33', pin='22344')
        melds = [self.__make_meld(Meld.CHII, sou='123')]
        self.assertRaises(
            NoYakuError,
            HandCalculator.calculate_hand_score, tiles, win_tile, melds=melds
        )

    def test_chinitsu(self):
        tiles = Tiles.string_to_array(man='1234567677889')
        win_tile = self.__string_to_tile_index(man='1')
        result = HandCalculator.calculate_hand_score(tiles, win_tile)
        self.assertEqual(result['han'], 6)
        self.assertEqual(result['fu'], 40)
        self.assertEqual(len(result['han_details']), 1)

        tiles = Tiles.string_to_array(man='1234567789')
        melds = [self.__make_meld(Meld.CHII, man='678')]
        result = HandCalculator.calculate_hand_score(
            tiles, win_tile, melds=melds)
        self.assertEqual(result['han'], 5)
        self.assertEqual(result['fu'], 30)
        self.assertEqual(len(result['han_details']), 1)

    def test_nagashi_mangan(self):
        tiles = Tiles.string_to_array(sou='13579', man='234456', pin='66')
        result = HandCalculator.calculate_hand_score(
            tiles, None, hand_config=HandConfig(is_nagashi_mangan=True))
        self.assertEqual(result['han'], 5)
        self.assertEqual(len(result['han_details']), 1)

    def test_dora(self):
        # hand without yaku, but with dora should be consider as invalid
        tiles = Tiles.string_to_array(sou='34', man='456789', honours='55')
        win_tile = self.__string_to_tile_index(sou='5')
        dora_indicators = [self.__string_to_tile_index(sou='5')]
        melds = [self.__make_meld(Meld.CHII, sou='678')]
        self.assertRaises(
            NoYakuError,
            HandCalculator.calculate_hand_score, tiles, win_tile,
            dora_indicators=dora_indicators, melds=melds)

        tiles = Tiles.string_to_array(sou='123456', man='12345', pin='33')
        win_tile = self.__string_to_tile_index(man='6')
        dora_indicators = [self.__string_to_tile_index(pin='2')]
        result = HandCalculator.calculate_hand_score(
            tiles, win_tile, dora_indicators=dora_indicators)
        self.assertEqual(result['han'], 3)
        self.assertEqual(result['fu'], 30)
        self.assertEqual(len(result['han_details']), 2)

        tiles = Tiles.string_to_array(man='2456678', pin='123678')
        win_tile = self.__string_to_tile_index(man='2')
        dora_indicators = [self.__string_to_tile_index(man='1'),
                           self.__string_to_tile_index(pin='2')]
        result = HandCalculator.calculate_hand_score(
            tiles, win_tile, dora_indicators=dora_indicators,
            hand_config=HandConfig(is_tsumo=True)
        )
        self.assertEqual(result['han'], 4)
        self.assertEqual(result['fu'], 30)
        self.assertEqual(len(result['han_details']), 2)

        # double dora
        tiles = Tiles.string_to_array(man='678', pin='3457', sou='123345')
        win_tile = self.__string_to_tile_index(pin='7')
        dora_indicators = [self.__string_to_tile_index(sou='4'),
                           self.__string_to_tile_index(sou='4')]
        result = HandCalculator.calculate_hand_score(
            tiles, win_tile, dora_indicators=dora_indicators,
            hand_config=HandConfig(is_tsumo=True)
        )
        self.assertEqual(result['han'], 3)
        self.assertEqual(result['fu'], 30)
        self.assertEqual(len(result['han_details']), 2)

        # double dora and honour tiles
        tiles = Tiles.string_to_array(man='678', pin='34', sou='123345',
                                      honours='66')
        win_tile = self.__string_to_tile_index(pin='5')
        dora_indicators = [self.__string_to_tile_index(honours='5'),
                           self.__string_to_tile_index(honours='5')]
        result = HandCalculator.calculate_hand_score(
            tiles, win_tile, dora_indicators=dora_indicators,
            hand_config=HandConfig(is_riichi=True)
        )
        self.assertEqual(result['han'], 5)
        self.assertEqual(result['fu'], 40)
        self.assertEqual(len(result['han_details']), 2)

        # double dora indicators and red dora
        tiles = Tiles.string_to_array(sou='123406', man='123678', pin='4')
        win_tile = self.__string_to_tile_index(pin='4')
        dora_indicators = [self.__string_to_tile_index(pin='2'),
                           self.__string_to_tile_index(pin='2')]
        result = HandCalculator.calculate_hand_score(
            tiles,
            win_tile,
            dora_indicators=dora_indicators,
            hand_config=HandConfig(is_tsumo=True)
        )
        self.assertEqual(result['han'], 2)
        self.assertEqual(result['fu'], 30)
        self.assertEqual(len(result['han_details']), 2)

        # dora in kan
        tiles = Tiles.string_to_array(pin='3457', sou='123345')
        win_tile = self.__string_to_tile_index(pin='7')
        melds = [self.__make_meld(Meld.KAN, is_open=False, man='7777')]
        dora_indicators = [self.__string_to_tile_index(man='6')]
        result = HandCalculator.calculate_hand_score(
            tiles, win_tile, dora_indicators=dora_indicators, melds=melds,
            hand_config=HandConfig(is_tsumo=True)
        )
        self.assertEqual(result['han'], 5)
        self.assertEqual(result['fu'], 40)
        self.assertEqual(len(result['han_details']), 2)

    def test_red_dora(self):
        # no red dora
        tiles = Tiles.string_to_array(sou='345', pin='456', man='1235559')
        win_tile = self.__string_to_tile_index(man='9')
        hand_config = HandConfig(is_tsumo=True)
        result = HandCalculator.calculate_hand_score(
            tiles, win_tile, hand_config=hand_config)
        self.assertEqual(result['han'], 1)

        # one red dora
        tiles = Tiles.string_to_array(sou='340', pin='456', man='1235559')
        result = HandCalculator.calculate_hand_score(
            tiles, win_tile, hand_config=hand_config)
        self.assertEqual(result['han'], 2)

        # two red dora
        tiles = Tiles.string_to_array(sou='340', pin='406', man='1235559')
        result = HandCalculator.calculate_hand_score(
            tiles, win_tile, hand_config=hand_config)
        self.assertEqual(result['han'], 3)

        # three red dora
        tiles = Tiles.string_to_array(sou='340', pin='406', man='1230559')
        result = HandCalculator.calculate_hand_score(
            tiles, win_tile, hand_config=hand_config)
        self.assertEqual(result['han'], 4)

        # four red dora
        tiles = Tiles.string_to_array(sou='340', pin='406', man='1230059')
        result = HandCalculator.calculate_hand_score(
            tiles, win_tile, hand_config=hand_config)
        self.assertEqual(result['han'], 5)

        # five+ red dora (technically not legal in mahjong)
        tiles = Tiles.string_to_array(sou='340', pin='406', man='1230009')
        result = HandCalculator.calculate_hand_score(
            tiles, win_tile, hand_config=hand_config)
        self.assertEqual(result['han'], 6)

    def test_kazoe_yakuman(self):
        tiles = Tiles.string_to_array(man='4446667788')
        win_tile = self.__string_to_tile_index(man='7')
        melds = [
            self.__make_meld(Meld.KAN, man='2222', is_open=False)
        ]
        dora_indicators = [
            self.__string_to_tile_index(man='1'),
            self.__string_to_tile_index(man='1'),
            self.__string_to_tile_index(man='1'),
            self.__string_to_tile_index(man='1'),
        ]
        hand_config = HandConfig(is_riichi=True)
        result = HandCalculator.calculate_hand_score(
            tiles, win_tile, melds, dora_indicators, hand_config)
        self.assertEqual(result['han'], 28)
        self.assertEqual(result['total_score'], 32000)


if __name__ == '__main__':
    unittest.main()
