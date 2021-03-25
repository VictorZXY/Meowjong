import numpy as np
import tensorflow as tf
from tensorflow import keras

from evaluation.agents.agent import Agent
from evaluation.hand_calculation.tile_constants import YAOCHUUHAI, EAST


class SLAgent(Agent):
    def __init__(self, wind, discard_model_path, pon_model_path, kan_model_path,
                 kita_model_path, riichi_model_path):
        super().__init__(wind=wind)
        self.discard_model = keras.models.load_model(discard_model_path)
        self.pon_model = keras.models.load_model(pon_model_path)
        self.kan_model = keras.models.load_model(kan_model_path)
        self.kita_model = keras.models.load_model(kita_model_path)
        self.riichi_model = keras.models.load_model(riichi_model_path)

    def eval_discard(self, target_tile, player1, player2, player3,
                     scores, round_number, honba_number, deposit_number,
                     dora_indicators):
        state = np.concatenate((
            Agent.encode_tile(target_tile),
            self.hand,
            self.red_dora,
            self.melds,
            self.kita,
            self.discards,
            dora_indicators,
            player1.encode_riichi_status(),
            player2.encode_riichi_status(),
            player3.encode_riichi_status(),
            scores,
            Agent.encode_round_number(round_number),
            Agent.encode_honba_number(honba_number),
            Agent.encode_deposit_number(deposit_number),
            self.wind,
            player1.melds,
            player1.kita,
            player1.discards,
            player2.melds,
            player2.kita,
            player2.discards,
            player3.melds,
            player3.kita,
            player3.discards
        ), axis=1).astype(tf.float32)
        state = tf.stack(state)
        return self.discard_model.predict(state)

    def eval_pon(self, target_tile, player1, player2, player3,
                 scores, round_number, honba_number, deposit_number,
                 dora_indicators):
        state = np.concatenate((
            Agent.encode_tile(target_tile),
            self.hand,
            self.red_dora,
            self.melds,
            self.kita,
            self.discards,
            dora_indicators,
            player1.encode_riichi_status(),
            player2.encode_riichi_status(),
            player3.encode_riichi_status(),
            scores,
            Agent.encode_round_number(round_number),
            Agent.encode_honba_number(honba_number),
            Agent.encode_deposit_number(deposit_number),
            self.wind,
            player1.melds,
            player1.kita,
            player1.discards,
            player2.melds,
            player2.kita,
            player2.discards,
            player3.melds,
            player3.kita,
            player3.discards
        ), axis=1).astype(tf.float32)
        state = tf.stack(state)
        return self.pon_model.predict(state)

    def eval_kan(self, target_tile, player1, player2, player3,
                 scores, round_number, honba_number, deposit_number,
                 dora_indicators):
        state = np.concatenate((
            Agent.encode_tile(target_tile),
            self.hand,
            self.red_dora,
            self.melds,
            self.kita,
            self.discards,
            dora_indicators,
            player1.encode_riichi_status(),
            player2.encode_riichi_status(),
            player3.encode_riichi_status(),
            scores,
            Agent.encode_round_number(round_number),
            Agent.encode_honba_number(honba_number),
            Agent.encode_deposit_number(deposit_number),
            self.wind,
            player1.melds,
            player1.kita,
            player1.discards,
            player2.melds,
            player2.kita,
            player2.discards,
            player3.melds,
            player3.kita,
            player3.discards
        ), axis=1).astype(tf.float32)
        state = tf.stack(state)
        return self.kan_model.predict(state)

    def eval_kita(self, target_tile, player1, player2, player3,
                  scores, round_number, honba_number, deposit_number,
                  dora_indicators):
        state = np.concatenate((
            Agent.encode_tile(target_tile),
            self.hand,
            self.red_dora,
            self.melds,
            self.kita,
            self.discards,
            dora_indicators,
            player1.encode_riichi_status(),
            player2.encode_riichi_status(),
            player3.encode_riichi_status(),
            scores,
            Agent.encode_round_number(round_number),
            Agent.encode_honba_number(honba_number),
            Agent.encode_deposit_number(deposit_number),
            self.wind,
            player1.melds,
            player1.kita,
            player1.discards,
            player2.melds,
            player2.kita,
            player2.discards,
            player3.melds,
            player3.kita,
            player3.discards
        ), axis=1).astype(tf.float32)
        state = tf.stack(state)
        return self.kita_model.predict(state)

    def eval_riichi(self, target_tile, player1, player2, player3,
                    scores, round_number, honba_number, deposit_number,
                    dora_indicators):
        state = np.concatenate((
            Agent.encode_tile(target_tile),
            self.hand,
            self.red_dora,
            self.melds,
            self.kita,
            self.discards,
            dora_indicators,
            player1.encode_riichi_status(),
            player2.encode_riichi_status(),
            player3.encode_riichi_status(),
            scores,
            Agent.encode_round_number(round_number),
            Agent.encode_honba_number(honba_number),
            Agent.encode_deposit_number(deposit_number),
            self.wind,
            player1.melds,
            player1.kita,
            player1.discards,
            player2.melds,
            player2.kita,
            player2.discards,
            player3.melds,
            player3.kita,
            player3.discards
        ), axis=1).astype(tf.float32)
        state = tf.stack(state)
        return self.riichi_model.predict(state)

    def eval_kyuushu_kyuuhai(self, target_tile, player1, player2, player3,
                             scores, round_number, honba_number, deposit_number,
                             dora_indicators):
        yaochuuhai_count = np.sum(self.hand[YAOCHUUHAI, 0], dtype=np.int32)
        if target_tile in YAOCHUUHAI and self.hand[target_tile, 0] == 0:
            yaochuuhai_count += 1

        if yaochuuhai_count >= 11:
            return 1.0
        elif yaochuuhai_count == 10:
            max_score = max(player1.score, player2.score, player3.score)
            if (self.wind == EAST and max_score - self.score >= 48000) \
                    or (self.wind != EAST and max_score - self.score >= 32000):
                return 1.0
            else:
                return 0.0
        else:
            return 0.0
