import numpy as np

from evaluation.agents.agent import Agent
from evaluation.hand_calculation.tiles import Tiles


class RandomAgent(Agent):
    def eval_discard(self, target_tile):
        return np.random.choice(Tiles.matrices_to_array(self.hand)
                                + [target_tile])

    def eval_pon(self, target_tile):
        return np.random.uniform(0.0, 1.0)

    def eval_kan(self, target_tile):
        return np.random.uniform(0.0, 1.0)

    def eval_kita(self, target_tile):
        return np.random.uniform(0.0, 1.0)

    def eval_riichi(self, target_tile):
        return np.random.uniform(0.0, 1.0)

    def eval_kyuushu_kyuuhai(self, target_tile):
        return np.random.uniform(0.0, 1.0)

    def eval_win(self, target_tile):
        return 1.0
