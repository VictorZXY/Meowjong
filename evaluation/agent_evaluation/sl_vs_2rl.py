import argparse

import tensorflow as tf
from tensorflow import keras

from evaluation.agent_evaluation.simulator import simulate
from evaluation.agents.rl_agent import RLAgent
from evaluation.agents.sl_agent import SLAgent
from evaluation.hand_calculation.tile_constants import EAST, SOUTH, WEST


def sl_vs_2rl(args):
    wind = args.wind
    discard_sl_model_path = args.discard_sl_model_path
    discard_rl_model_path = args.discard_rl_model_path
    pon_model_path = args.pon_model_path
    kan_model_path = args.kan_model_path
    kita_model_path = args.kita_model_path
    riichi_model_path = args.riichi_model_path
    batch = args.batch

    discard_sl_model = keras.models.load_model(discard_sl_model_path)
    discard_rl_model = keras.models.load_model(discard_rl_model_path,
                                               compile=False)
    discard_rl_model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy'])
    pon_model = keras.models.load_model(pon_model_path)
    kan_model = keras.models.load_model(kan_model_path)
    kita_model = keras.models.load_model(kita_model_path)
    riichi_model = keras.models.load_model(riichi_model_path)

    sl_agent = SLAgent(
        wind=wind,
        discard_model=discard_sl_model,
        pon_model=pon_model,
        kan_model=kan_model,
        kita_model=kita_model,
        riichi_model=riichi_model
    )

    rl_agent_1 = RLAgent(
        wind=(wind + 1 - EAST) % 3 + EAST,
        discard_model=discard_rl_model,
        pon_model=pon_model,
        kan_model=kan_model,
        kita_model=kita_model,
        riichi_model=riichi_model
    )

    rl_agent_2 = RLAgent(
        wind=(wind + 2 - EAST) % 3 + EAST,
        discard_model=discard_rl_model,
        pon_model=pon_model,
        kan_model=kan_model,
        kita_model=kita_model,
        riichi_model=riichi_model
    )

    if wind == EAST:
        players = [sl_agent, rl_agent_1, rl_agent_2]
    elif wind == SOUTH:
        players = [rl_agent_2, sl_agent, rl_agent_1]
    elif wind == WEST:
        players = [rl_agent_1, rl_agent_2, sl_agent]

    for i in range((batch - 1) * 1000, batch * 1000):
        try:
            for index, player in enumerate(players):
                player.reset(wind=EAST + index)
            round_scores = simulate(players, seed=i)
            print(str(i) + ' '
                  + str(round_scores[0]) + ' '
                  + str(round_scores[1]) + ' '
                  + str(round_scores[2]))
        except:
            print(i, 'ILLEGAL DISCARDS')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--wind', action='store', type=int, required=True)
    parser.add_argument('--discard_sl_model_path', action='store', type=str,
                        required=True)
    parser.add_argument('--discard_rl_model_path', action='store', type=str,
                        required=True)
    parser.add_argument('--pon_model_path', action='store', type=str,
                        required=True)
    parser.add_argument('--kan_model_path', action='store', type=str,
                        required=True)
    parser.add_argument('--kita_model_path', action='store', type=str,
                        required=True)
    parser.add_argument('--riichi_model_path', action='store', type=str,
                        required=True)
    parser.add_argument('--batch', action='store', type=int, required=True)
    args = parser.parse_args()

    sl_vs_2rl(args)
