import unittest

from hand_calculation.agari import Agari
from hand_calculation.meld import Meld
from hand_calculation.tiles import Tiles


class AgariSimpleTestCase(unittest.TestCase):
    def test_is_agari(self):
        agari = Agari()

        tiles = Tiles.string_to_array(sou='123456789', pin='123', man='33')
        self.assertTrue(agari.is_agari_simple(tiles))

        tiles = Tiles.string_to_array(sou='123456789', pin='11123')
        self.assertTrue(agari.is_agari_simple(tiles))

        tiles = Tiles.string_to_array(sou='123456789', honours='11777')
        self.assertTrue(agari.is_agari_simple(tiles))

        tiles = Tiles.string_to_array(sou='12345556778899')
        self.assertTrue(agari.is_agari_simple(tiles))

        tiles = Tiles.string_to_array(sou='11123456788999')
        self.assertTrue(agari.is_agari_simple(tiles))

        tiles = Tiles.string_to_array(sou='233334', pin='789', man='345',
                                      honours='55')
        self.assertTrue(agari.is_agari_simple(tiles))

    def test_is_not_agari(self):
        agari = Agari()

        tiles = Tiles.string_to_array(sou='123456789', pin='12345')
        self.assertFalse(agari.is_agari_simple(tiles))

        tiles = Tiles.string_to_array(sou='111222444', pin='11145')
        self.assertFalse(agari.is_agari_simple(tiles))

        tiles = Tiles.string_to_array(sou='11122233356888')
        self.assertFalse(agari.is_agari_simple(tiles))

    def test_is_chitoitsu_agari(self):
        agari = Agari()

        tiles = Tiles.string_to_array(sou='1133557799', pin='1199')
        self.assertTrue(agari.is_agari_simple(tiles))

        tiles = Tiles.string_to_array(sou='2244', pin='1199', man='11',
                                      honours='2277')
        self.assertTrue(agari.is_agari_simple(tiles))

        tiles = Tiles.string_to_array(man='11223344556677')
        self.assertTrue(agari.is_agari_simple(tiles))

    def test_is_kokushi_musou_agari(self):
        agari = Agari()

        tiles = Tiles.string_to_array(sou='19', pin='19', man='199',
                                      honours='1234567')
        self.assertTrue(agari.is_agari_simple(tiles))

        tiles = Tiles.string_to_array(sou='19', pin='19', man='19',
                                      honours='11234567')
        self.assertTrue(agari.is_agari_simple(tiles))

        tiles = Tiles.string_to_array(sou='19', pin='19', man='19',
                                      honours='12345677')
        self.assertTrue(agari.is_agari_simple(tiles))

        tiles = Tiles.string_to_array(sou='129', pin='19', man='19',
                                      honours='1234567')
        self.assertFalse(agari.is_agari_simple(tiles))

        tiles = Tiles.string_to_array(sou='19', pin='19', man='19',
                                      honours='11134567')
        self.assertFalse(agari.is_agari_simple(tiles))

    def test_is_agari_and_open_hand(self):
        agari = Agari()

        tiles = Tiles.string_to_array(sou='23467', pin='222')
        melds = [
            Meld(Meld.CHII, tiles='345m'),
            Meld(Meld.CHII, tiles='555s')
        ]
        self.assertFalse(agari.is_agari_simple(tiles, melds))


if __name__ == '__main__':
    unittest.main()
