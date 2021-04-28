import argparse

import numpy as np
import tensorflow as tf
from tensorflow import keras

from evaluation.agents.agent import Agent
from evaluation.game_simulator.simulator import simulate
from evaluation.hand_calculation.tile_constants import YAOCHUUHAI, EAST, SOUTH, \
    WEST, TILES_COUNT

assert tf.__version__ >= "2.0"

# To make the output stable across runs
np.random.seed(42)
tf.random.set_seed(42)


class REINFORCEAgent(Agent):
    def __init__(self, wind, discard_model_path='', pon_model_path='',
                 kan_model_path='', kita_model_path='', riichi_model_path='',
                 discard_model=None, pon_model=None, kan_model=None,
                 kita_model=None, riichi_model=None):
        super().__init__(wind=wind)

        if discard_model is not None and discard_model_path == '':
            self.discard_model = discard_model
            self.pon_model = pon_model
            self.kan_model = kan_model
            self.kita_model = kita_model
            self.riichi_model = riichi_model
        elif discard_model_path != '' and discard_model is None:
            self.discard_model = keras.models.load_model(discard_model_path,
                                                         compile=False)
            self.pon_model = keras.models.load_model(pon_model_path)
            self.kan_model = keras.models.load_model(kan_model_path)
            self.kita_model = keras.models.load_model(kita_model_path)
            self.riichi_model = keras.models.load_model(riichi_model_path)
        else:
            raise ValueError

        # Hyperparameters for the policy gradient methods
        self.discount_factor = 0.99
        self.learning_rate = 1e-3

        # Lists for the states and actions
        # (the reward is always 0 until the end of the round)
        self.states = []
        self.actions = []

        # Using categorical crossentropy as a loss is a trick to easily
        # implement the policy gradient. Categorical cross entropy is defined
        # H(p, q) = sum(p_i * log(q_i)). For the action taken (a), set
        # p_a = expected return (G_t), and q_a = output of the policy network,
        # which is the probability of taking the action a, i.e. pi(a | s).
        # All other p_i are zero, thus we have H(p, q) = G_t * log(pi(a | s)).
        self.discard_model.compile(
            loss="categorical_crossentropy",
            optimizer=tf.keras.optimizers.Adam(learning_rate=self.learning_rate)
        )

    def reset(self, wind=None, score=35000):
        super().reset(wind=wind, score=score)
        self.states = []
        self.actions = []

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
            Agent.encode_tile(self.wind),
            player1.melds,
            player1.kita,
            player1.discards,
            player2.melds,
            player2.kita,
            player2.discards,
            player3.melds,
            player3.kita,
            player3.discards
        ), axis=1).astype(np.float32)
        state = tf.stack(state)
        state = tf.reshape(state, [1, 34, 366, 1])

        # Using the output of the policy network, pick action stochastically
        policy = self.discard_model.predict(state).flatten()
        action = np.random.choice(TILES_COUNT, p=policy)

        # Save the state and action
        self.states.append(state[0])
        self.actions.append(action)

        # Output the chosen action
        return action

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
            Agent.encode_tile(self.wind),
            player1.melds,
            player1.kita,
            player1.discards,
            player2.melds,
            player2.kita,
            player2.discards,
            player3.melds,
            player3.kita,
            player3.discards
        ), axis=1).astype(np.float32)
        state = tf.stack(state)
        state = tf.reshape(state, [1, 34, 366, 1])
        return self.pon_model.predict(state)[0][1]

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
            Agent.encode_tile(self.wind),
            player1.melds,
            player1.kita,
            player1.discards,
            player2.melds,
            player2.kita,
            player2.discards,
            player3.melds,
            player3.kita,
            player3.discards
        ), axis=1).astype(np.float32)
        state = tf.stack(state)
        state = tf.reshape(state, [1, 34, 366, 1])
        return self.kan_model.predict(state)[0][1]

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
            Agent.encode_tile(self.wind),
            player1.melds,
            player1.kita,
            player1.discards,
            player2.melds,
            player2.kita,
            player2.discards,
            player3.melds,
            player3.kita,
            player3.discards
        ), axis=1).astype(np.float32)
        state = tf.stack(state)
        state = tf.reshape(state, [1, 34, 366, 1])
        return self.kita_model.predict(state)[0][1]

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
            Agent.encode_tile(self.wind),
            player1.melds,
            player1.kita,
            player1.discards,
            player2.melds,
            player2.kita,
            player2.discards,
            player3.melds,
            player3.kita,
            player3.discards
        ), axis=1).astype(np.float32)
        state = tf.stack(state)
        state = tf.reshape(state, [1, 34, 366, 1])
        return self.riichi_model.predict(state)[0][1]

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

    def discount_rewards(self, final_reward):
        discounted_returns = np.zeros_like(self.actions)
        discounted_returns[-1] = final_reward
        for t in reversed(range(len(discounted_returns) - 1)):
            discounted_returns[t] = self.discount_factor \
                                    * discounted_returns[t + 1]
        return (discounted_returns - np.mean(discounted_returns)) \
               / np.std(discounted_returns)

    def train_discard_model(self, all_states, all_actions,
                            all_discounted_returns):
        episode_length = len(all_states)
        update_inputs = tf.stack(all_states)
        expected_returns = np.zeros((episode_length, TILES_COUNT))
        for i in range(episode_length):
            expected_returns[i][all_actions[i]] = all_discounted_returns[i]
        self.discard_model.fit(update_inputs, expected_returns, epochs=1,
                               verbose=0)

    def update_discard_model(self, new_discard_model):
        self.discard_model = new_discard_model


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--discard_model_path', action='store', type=str,
                        required=True)
    parser.add_argument('--pon_model_path', action='store', type=str,
                        required=True)
    parser.add_argument('--kan_model_path', action='store', type=str,
                        required=True)
    parser.add_argument('--kita_model_path', action='store', type=str,
                        required=True)
    parser.add_argument('--riichi_model_path', action='store', type=str,
                        required=True)

    args = parser.parse_args()
    discard_model_path = args.discard_model_path
    pon_model_path = args.pon_model_path
    kan_model_path = args.kan_model_path
    kita_model_path = args.kita_model_path
    riichi_model_path = args.riichi_model_path

    discard_model = keras.models.load_model(discard_model_path, compile=False)
    pon_model = keras.models.load_model(pon_model_path)
    kan_model = keras.models.load_model(kan_model_path)
    kita_model = keras.models.load_model(kita_model_path)
    riichi_model = keras.models.load_model(riichi_model_path)

    REINFORCE_agent_east = REINFORCEAgent(
        wind=EAST,
        discard_model=discard_model,
        pon_model=pon_model,
        kan_model=kan_model,
        kita_model=kita_model,
        riichi_model=riichi_model
    )

    REINFORCE_agent_south = REINFORCEAgent(
        wind=SOUTH,
        discard_model=discard_model,
        pon_model=pon_model,
        kan_model=kan_model,
        kita_model=kita_model,
        riichi_model=riichi_model
    )

    REINFORCE_agent_west = REINFORCEAgent(
        wind=WEST,
        discard_model=discard_model,
        pon_model=pon_model,
        kan_model=kan_model,
        kita_model=kita_model,
        riichi_model=riichi_model
    )

    players = [REINFORCE_agent_east,
               REINFORCE_agent_south,
               REINFORCE_agent_west]

    episodes = 5

    i = 0
    seed = 0
    while i < episodes:
        for index, player in enumerate(players):
            player.reset(wind=EAST + index)

        round_scores = simulate(players, seed=seed)

        seed += 1
        if round_scores[0] == round_scores[1] == round_scores[2] == 0:
            continue

        print(str(i) + ' '
              + str(round_scores[0]) + ' '
              + str(round_scores[1]) + ' '
              + str(round_scores[2]))

        all_states = [*REINFORCE_agent_east.states,
                      *REINFORCE_agent_south.states,
                      *REINFORCE_agent_west.states]
        all_actions = [*REINFORCE_agent_east.actions,
                       *REINFORCE_agent_south.actions,
                       *REINFORCE_agent_west.actions]
        discounted_returns_east = REINFORCE_agent_east.discount_rewards(
            round_scores[0])
        discounted_returns_south = REINFORCE_agent_east.discount_rewards(
            round_scores[1])
        discounted_returns_west = REINFORCE_agent_east.discount_rewards(
            round_scores[2])
        all_discounted_returns = [*discounted_returns_east,
                                  *discounted_returns_south,
                                  *discounted_returns_west]
        print(all_discounted_returns)

        REINFORCE_agent_east.train_discard_model(
            all_states=all_states,
            all_actions=all_actions,
            all_discounted_returns=all_discounted_returns
        )
        REINFORCE_agent_south.update_discard_model(
            REINFORCE_agent_east.discard_model)
        REINFORCE_agent_west.update_discard_model(
            REINFORCE_agent_east.discard_model)

        i += 1
