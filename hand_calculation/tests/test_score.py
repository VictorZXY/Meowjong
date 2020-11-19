import unittest

from hand_calculation.hand_config import HandConfig
from hand_calculation.score import Score
from hand_calculation.tile_constants import EAST, SOUTH, WEST


class ScoreTestCase(unittest.TestCase):
    def test_calculate_ron_score(self):
        hand_config = HandConfig()

        result = Score.calculate_score(han=1, fu=30, hand_config=hand_config)
        self.assertEqual(result["total_score"], 1000)

        result = Score.calculate_score(han=1, fu=110, hand_config=hand_config)
        self.assertEqual(result["total_score"], 3600)

        result = Score.calculate_score(han=2, fu=30, hand_config=hand_config)
        self.assertEqual(result["total_score"], 2000)

        result = Score.calculate_score(han=3, fu=30, hand_config=hand_config)
        self.assertEqual(result["total_score"], 3900)

        result = Score.calculate_score(han=4, fu=30, hand_config=hand_config)
        self.assertEqual(result["total_score"], 7700)

        result = Score.calculate_score(han=4, fu=40, hand_config=hand_config)
        self.assertEqual(result["total_score"], 8000)

        result = Score.calculate_score(han=5, fu=0, hand_config=hand_config)
        self.assertEqual(result["total_score"], 8000)

        result = Score.calculate_score(han=6, fu=0, hand_config=hand_config)
        self.assertEqual(result["total_score"], 12000)

        result = Score.calculate_score(han=8, fu=0, hand_config=hand_config)
        self.assertEqual(result["total_score"], 16000)

        result = Score.calculate_score(han=11, fu=0, hand_config=hand_config)
        self.assertEqual(result["total_score"], 24000)

        result = Score.calculate_score(han=13, fu=0, hand_config=hand_config)
        self.assertEqual(result["total_score"], 32000)

        result = Score.calculate_score(han=26, fu=0, hand_config=hand_config)
        self.assertEqual(result["total_score"], 32000)

        result = Score.calculate_score(han=39, fu=0, hand_config=hand_config)
        self.assertEqual(result["total_score"], 32000)

        result = Score.calculate_score(han=52, fu=0, hand_config=hand_config)
        self.assertEqual(result["total_score"], 32000)

        result = Score.calculate_score(han=65, fu=0, hand_config=hand_config)
        self.assertEqual(result["total_score"], 32000)

        result = Score.calculate_score(han=78, fu=0, hand_config=hand_config)
        self.assertEqual(result["total_score"], 32000)

    def test_calculate_dealer_ron_score(self):
        hand_config = HandConfig(seat_wind=EAST)

        result = Score.calculate_score(han=1, fu=30, hand_config=hand_config)
        self.assertEqual(result["total_score"], 1500)

        result = Score.calculate_score(han=2, fu=30, hand_config=hand_config)
        self.assertEqual(result["total_score"], 2900)

        result = Score.calculate_score(han=3, fu=30, hand_config=hand_config)
        self.assertEqual(result["total_score"], 5800)

        result = Score.calculate_score(han=4, fu=30, hand_config=hand_config)
        self.assertEqual(result["total_score"], 11600)

        result = Score.calculate_score(han=5, fu=0, hand_config=hand_config)
        self.assertEqual(result["total_score"], 12000)

        result = Score.calculate_score(han=6, fu=0, hand_config=hand_config)
        self.assertEqual(result["total_score"], 18000)

        result = Score.calculate_score(han=8, fu=0, hand_config=hand_config)
        self.assertEqual(result["total_score"], 24000)

        result = Score.calculate_score(han=11, fu=0, hand_config=hand_config)
        self.assertEqual(result["total_score"], 36000)

        result = Score.calculate_score(han=13, fu=0, hand_config=hand_config)
        self.assertEqual(result["total_score"], 48000)

        result = Score.calculate_score(han=26, fu=0, hand_config=hand_config)
        self.assertEqual(result["total_score"], 48000)

        result = Score.calculate_score(han=39, fu=0, hand_config=hand_config)
        self.assertEqual(result["total_score"], 48000)

        result = Score.calculate_score(han=52, fu=0, hand_config=hand_config)
        self.assertEqual(result["total_score"], 48000)

        result = Score.calculate_score(han=65, fu=0, hand_config=hand_config)
        self.assertEqual(result["total_score"], 48000)

        result = Score.calculate_score(han=78, fu=0, hand_config=hand_config)
        self.assertEqual(result["total_score"], 48000)

    def test_calculate_tsumo_score(self):
        hand_config = HandConfig(is_tsumo=True)

        result = Score.calculate_score(han=1, fu=30, hand_config=hand_config)
        self.assertEqual(result["total_score"], 1100)

        result = Score.calculate_score(han=3, fu=30, hand_config=hand_config)
        self.assertEqual(result["total_score"], 4000)

        result = Score.calculate_score(han=3, fu=60, hand_config=hand_config)
        self.assertEqual(result["total_score"], 7900)

        result = Score.calculate_score(han=4, fu=30, hand_config=hand_config)
        self.assertEqual(result["total_score"], 7900)

        result = Score.calculate_score(han=5, fu=0, hand_config=hand_config)
        self.assertEqual(result["total_score"], 8000)

        result = Score.calculate_score(han=6, fu=0, hand_config=hand_config)
        self.assertEqual(result["total_score"], 12000)

        result = Score.calculate_score(han=8, fu=0, hand_config=hand_config)
        self.assertEqual(result["total_score"], 16000)

        result = Score.calculate_score(han=11, fu=0, hand_config=hand_config)
        self.assertEqual(result["total_score"], 24000)

        result = Score.calculate_score(han=13, fu=0, hand_config=hand_config)
        self.assertEqual(result["total_score"], 32000)

        result = Score.calculate_score(han=26, fu=0, hand_config=hand_config)
        self.assertEqual(result["total_score"], 32000)

        result = Score.calculate_score(han=39, fu=0, hand_config=hand_config)
        self.assertEqual(result["total_score"], 32000)

        result = Score.calculate_score(han=52, fu=0, hand_config=hand_config)
        self.assertEqual(result["total_score"], 32000)

        result = Score.calculate_score(han=65, fu=0, hand_config=hand_config)
        self.assertEqual(result["total_score"], 32000)

        result = Score.calculate_score(han=78, fu=0, hand_config=hand_config)
        self.assertEqual(result["total_score"], 32000)

    def test_calculate_dealer_tsumo_score(self):
        hand_config = HandConfig(seat_wind=EAST, is_tsumo=True)

        result = Score.calculate_score(han=1, fu=30, hand_config=hand_config)
        self.assertEqual(result["total_score"], 1500)

        result = Score.calculate_score(han=3, fu=30, hand_config=hand_config)
        self.assertEqual(result["total_score"], 6000)

        result = Score.calculate_score(han=4, fu=30, hand_config=hand_config)
        self.assertEqual(result["total_score"], 11700)

        result = Score.calculate_score(han=5, fu=0, hand_config=hand_config)
        self.assertEqual(result["total_score"], 12000)

        result = Score.calculate_score(han=6, fu=0, hand_config=hand_config)
        self.assertEqual(result["total_score"], 18000)

        result = Score.calculate_score(han=8, fu=0, hand_config=hand_config)
        self.assertEqual(result["total_score"], 24000)

        result = Score.calculate_score(han=11, fu=0, hand_config=hand_config)
        self.assertEqual(result["total_score"], 36000)

        result = Score.calculate_score(han=13, fu=0, hand_config=hand_config)
        self.assertEqual(result["total_score"], 48000)

        result = Score.calculate_score(han=26, fu=0, hand_config=hand_config)
        self.assertEqual(result["total_score"], 48000)

        result = Score.calculate_score(han=39, fu=0, hand_config=hand_config)
        self.assertEqual(result["total_score"], 48000)

        result = Score.calculate_score(han=52, fu=0, hand_config=hand_config)
        self.assertEqual(result["total_score"], 48000)

        result = Score.calculate_score(han=65, fu=0, hand_config=hand_config)
        self.assertEqual(result["total_score"], 48000)

        result = Score.calculate_score(han=78, fu=0, hand_config=hand_config)
        self.assertEqual(result["total_score"], 48000)

    def test_calculate_sanma_tsumo_score(self):
        hand_config = HandConfig(is_sanma=True, is_tsumo=True)

        result = Score.calculate_score(han=1, fu=30, hand_config=hand_config)
        self.assertEqual(result["total_score"], 800)

        result = Score.calculate_score(han=3, fu=30, hand_config=hand_config)
        self.assertEqual(result["total_score"], 3000)

        result = Score.calculate_score(han=3, fu=60, hand_config=hand_config)
        self.assertEqual(result["total_score"], 5900)

        result = Score.calculate_score(han=4, fu=30, hand_config=hand_config)
        self.assertEqual(result["total_score"], 5900)

        result = Score.calculate_score(han=5, fu=0, hand_config=hand_config)
        self.assertEqual(result["total_score"], 6000)

        result = Score.calculate_score(han=6, fu=0, hand_config=hand_config)
        self.assertEqual(result["total_score"], 9000)

        result = Score.calculate_score(han=8, fu=0, hand_config=hand_config)
        self.assertEqual(result["total_score"], 12000)

        result = Score.calculate_score(han=11, fu=0, hand_config=hand_config)
        self.assertEqual(result["total_score"], 18000)

        result = Score.calculate_score(han=13, fu=0, hand_config=hand_config)
        self.assertEqual(result["total_score"], 24000)

        result = Score.calculate_score(han=26, fu=0, hand_config=hand_config)
        self.assertEqual(result["total_score"], 24000)

        result = Score.calculate_score(han=39, fu=0, hand_config=hand_config)
        self.assertEqual(result["total_score"], 24000)

        result = Score.calculate_score(han=52, fu=0, hand_config=hand_config)
        self.assertEqual(result["total_score"], 24000)

        result = Score.calculate_score(han=65, fu=0, hand_config=hand_config)
        self.assertEqual(result["total_score"], 24000)

        result = Score.calculate_score(han=78, fu=0, hand_config=hand_config)
        self.assertEqual(result["total_score"], 24000)

    def test_calculate_sanma_dealer_tsumo_score(self):
        hand_config = HandConfig(seat_wind=EAST, is_sanma=True, is_tsumo=True)

        result = Score.calculate_score(han=1, fu=30, hand_config=hand_config)
        self.assertEqual(result["total_score"], 1000)

        result = Score.calculate_score(han=3, fu=30, hand_config=hand_config)
        self.assertEqual(result["total_score"], 4000)

        result = Score.calculate_score(han=4, fu=30, hand_config=hand_config)
        self.assertEqual(result["total_score"], 7800)

        result = Score.calculate_score(han=5, fu=0, hand_config=hand_config)
        self.assertEqual(result["total_score"], 8000)

        result = Score.calculate_score(han=6, fu=0, hand_config=hand_config)
        self.assertEqual(result["total_score"], 12000)

        result = Score.calculate_score(han=8, fu=0, hand_config=hand_config)
        self.assertEqual(result["total_score"], 16000)

        result = Score.calculate_score(han=11, fu=0, hand_config=hand_config)
        self.assertEqual(result["total_score"], 24000)

        result = Score.calculate_score(han=13, fu=0, hand_config=hand_config)
        self.assertEqual(result["total_score"], 32000)

        result = Score.calculate_score(han=26, fu=0, hand_config=hand_config)
        self.assertEqual(result["total_score"], 32000)

        result = Score.calculate_score(han=39, fu=0, hand_config=hand_config)
        self.assertEqual(result["total_score"], 32000)

        result = Score.calculate_score(han=52, fu=0, hand_config=hand_config)
        self.assertEqual(result["total_score"], 32000)

        result = Score.calculate_score(han=65, fu=0, hand_config=hand_config)
        self.assertEqual(result["total_score"], 32000)

        result = Score.calculate_score(han=78, fu=0, hand_config=hand_config)
        self.assertEqual(result["total_score"], 32000)

    def test_calculate_score_with_bonus(self):
        hand_config = HandConfig(seat_wind=EAST, is_tsumo=True,
                                 deposit_counter=3, honba_counter=2)
        result = Score.calculate_score(han=3, fu=30, hand_config=hand_config)
        self.assertEqual(result["total_score"], 9600)

        hand_config = HandConfig(seat_wind=WEST, is_sanma=True, is_tsumo=True,
                                 deposit_counter=1, honba_counter=4)
        result = Score.calculate_score(han=4, fu=30, hand_config=hand_config)
        self.assertEqual(result["total_score"], 7700)

        hand_config = HandConfig(seat_wind=WEST, honba_counter=5)
        result = Score.calculate_score(han=6, fu=30, hand_config=hand_config)
        self.assertEqual(result["total_score"], 13500)

        hand_config = HandConfig(seat_wind=EAST, is_sanma=True,
                                 honba_counter=5)
        result = Score.calculate_score(han=5, fu=30, hand_config=hand_config)
        self.assertEqual(result["total_score"], 13000)

    def test_calculate_yakuman_score(self):
        hand_config = HandConfig(seat_wind=EAST, is_tsumo=True,
                                 deposit_counter=2, honba_counter=3)
        result = Score.calculate_yakuman_score(
            yakuman_list=['Kokushi Musou'],
            hand_config=hand_config
        )
        self.assertEqual(result['total_score'], 50900)

        hand_config = HandConfig(seat_wind=EAST, is_sanma=True, is_tsumo=True,
                                 deposit_counter=2, honba_counter=3)
        result = Score.calculate_yakuman_score(
            yakuman_list=['Ryuuiisou'],
            hand_config=hand_config
        )
        self.assertEqual(result['total_score'], 34600)

        hand_config = HandConfig(seat_wind=SOUTH, is_sanma=True,
                                 is_tsumo=True, deposit_counter=2,
                                 honba_counter=3)
        result = Score.calculate_yakuman_score(
            yakuman_list=['Junsei Chuuren Poutou'],
            hand_config=hand_config
        )
        self.assertEqual(result['total_score'], 26600)

        hand_config = HandConfig(seat_wind=EAST, is_sanma=True,
                                 deposit_counter=3)
        result = Score.calculate_yakuman_score(
            yakuman_list=['Tsuuiisou', 'Daisuushii', 'Suukantsu',
                          'Suuankou Tanki'],
            hand_config=hand_config
        )
        self.assertEqual(result['total_score'], 195000)
        self.assertEqual(result['yaku_level'], '4x Yakuman')


if __name__ == '__main__':
    unittest.main()
