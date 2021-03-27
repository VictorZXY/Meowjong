import numpy as np

from evaluation.agents.agent import Agent
from evaluation.hand_calculation.tiles import Tiles


class RandomAgent(Agent):
    def eval_discard(self, target_tile, player1, player2, player3,
                     scores, round_number, honba_number, deposit_number,
                     dora_indicators):
        return np.random.choice(Tiles.matrix_to_indices(self.hand)
                                + [target_tile])

    def eval_pon(self, target_tile, player1, player2, player3,
                 scores, round_number, honba_number, deposit_number,
                 dora_indicators):
        return np.random.choice([0.0, 1.0])

    def eval_kan(self, target_tile, player1, player2, player3,
                 scores, round_number, honba_number, deposit_number,
                 dora_indicators):
        return np.random.choice([0.0, 1.0])

    def eval_kita(self, target_tile, player1, player2, player3,
                  scores, round_number, honba_number, deposit_number,
                  dora_indicators):
        return np.random.choice([0.0, 1.0])

    def eval_riichi(self, target_tile, player1, player2, player3,
                    scores, round_number, honba_number, deposit_number,
                    dora_indicators):
        return np.random.choice([0.0, 1.0])

    def eval_kyuushu_kyuuhai(self, target_tile, player1, player2, player3,
                             scores, round_number, honba_number, deposit_number,
                             dora_indicators):
        return np.random.choice([0.0, 1.0])
