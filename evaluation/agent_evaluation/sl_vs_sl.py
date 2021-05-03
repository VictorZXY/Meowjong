import argparse

from tensorflow import keras

from evaluation.agent_evaluation.simulator import simulate
from evaluation.agents.sl_agent import SLAgent
from evaluation.hand_calculation.tile_constants import EAST, SOUTH, WEST


def sl_vs_sl(args):
    discard_model_path = args.discard_model_path
    pon_model_path = args.pon_model_path
    kan_model_path = args.kan_model_path
    kita_model_path = args.kita_model_path
    riichi_model_path = args.riichi_model_path
    batch = args.batch

    discard_model = keras.models.load_model(discard_model_path)
    pon_model = keras.models.load_model(pon_model_path)
    kan_model = keras.models.load_model(kan_model_path)
    kita_model = keras.models.load_model(kita_model_path)
    riichi_model = keras.models.load_model(riichi_model_path)

    sl_agent_east = SLAgent(
        wind=EAST,
        discard_model=discard_model,
        pon_model=pon_model,
        kan_model=kan_model,
        kita_model=kita_model,
        riichi_model=riichi_model
    )

    sl_agent_south = SLAgent(
        wind=SOUTH,
        discard_model=discard_model,
        pon_model=pon_model,
        kan_model=kan_model,
        kita_model=kita_model,
        riichi_model=riichi_model
    )

    sl_agent_west = SLAgent(
        wind=WEST,
        discard_model=discard_model,
        pon_model=pon_model,
        kan_model=kan_model,
        kita_model=kita_model,
        riichi_model=riichi_model
    )

    players = [sl_agent_east, sl_agent_south, sl_agent_west]

    for i in range((batch - 1) * 1000, batch * 1000):
        for index, player in enumerate(players):
            player.reset(wind=EAST + index)
        round_scores = simulate(players, seed=i)
        print(str(i) + ' '
              + str(round_scores[0]) + ' '
              + str(round_scores[1]) + ' '
              + str(round_scores[2]))


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
    parser.add_argument('--batch', action='store', type=int, required=True)
    args = parser.parse_args()

    sl_vs_sl(args)
