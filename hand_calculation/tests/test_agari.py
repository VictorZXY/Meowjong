import unittest

from hand_calculation import tile_constants
from hand_calculation.agari import Agari
from hand_calculation.meld import Meld
from hand_calculation.tiles import Tiles


class AgariTestCase(unittest.TestCase):
    def test_is_agari(self):
        agari = Agari()

        tiles = Tiles.string_to_array(man='123456789', pin='123', sou='33')
        self.assertTrue(agari.is_agari(tiles))

        tiles = Tiles.string_to_array(man='123456789', pin='11123')
        self.assertTrue(agari.is_agari(tiles))

        tiles = Tiles.string_to_array(man='123456789', honours='11777')
        self.assertTrue(agari.is_agari(tiles))

        tiles = Tiles.string_to_array(man='12345556778899')
        self.assertTrue(agari.is_agari(tiles))

        tiles = Tiles.string_to_array(man='11123456788999')
        self.assertTrue(agari.is_agari(tiles))

        tiles = Tiles.string_to_array(man='233334', pin='789', sou='345',
                                      honours='55')
        self.assertTrue(agari.is_agari(tiles))

    def test_is_not_agari(self):
        agari = Agari()

        tiles = Tiles.string_to_array(man='123456789', pin='12345')
        self.assertFalse(agari.is_agari(tiles))

        tiles = Tiles.string_to_array(man='111222444', pin='11145')
        self.assertFalse(agari.is_agari(tiles))

        tiles = Tiles.string_to_array(man='11122233356888')
        self.assertFalse(agari.is_agari(tiles))

    def test_is_chitoitsu_agari(self):
        agari = Agari()

        tiles = Tiles.string_to_array(man='1133557799', pin='1199')
        self.assertTrue(agari.is_agari(tiles))

        tiles = Tiles.string_to_array(man='2244', pin='1199', sou='11',
                                      honours='2277')
        self.assertTrue(agari.is_agari(tiles))

        tiles = Tiles.string_to_array(sou='11223344556677')
        self.assertTrue(agari.is_agari(tiles))

    def test_is_kokushi_muman_agari(self):
        agari = Agari()

        tiles = Tiles.string_to_array(man='19', pin='19', sou='199',
                                      honours='1234567')
        self.assertTrue(agari.is_agari(tiles))

        tiles = Tiles.string_to_array(man='19', pin='19', sou='19',
                                      honours='11234567')
        self.assertTrue(agari.is_agari(tiles))

        tiles = Tiles.string_to_array(man='19', pin='19', sou='19',
                                      honours='12345677')
        self.assertTrue(agari.is_agari(tiles))

        tiles = Tiles.string_to_array(man='129', pin='19', sou='19',
                                      honours='1234567')
        self.assertFalse(agari.is_agari(tiles))

        tiles = Tiles.string_to_array(man='19', pin='19', sou='19',
                                      honours='11134567')
        self.assertFalse(agari.is_agari(tiles))

    def test_is_agari_and_open_hand(self):
        agari = Agari()

        tiles = Tiles.string_to_array(man='23467', pin='222')
        melds = [
            Meld(Meld.CHII, tiles='345m'),
            Meld(Meld.CHII, tiles='555s')
        ]
        self.assertFalse(agari.is_agari(tiles, melds=melds))

        tiles = Tiles.string_to_array(pin="99", honours="77")
        win_tile = tile_constants.NINE_PIN
        melds = [
            Meld(Meld.PON, tiles="111z"),
            Meld(Meld.CHII, tiles="123p"),
            Meld(Meld.CHII, tiles="123p"),
        ]
        self.assertTrue(agari.is_agari(tiles, win_tile, melds=melds))


if __name__ == '__main__':
    unittest.main()
