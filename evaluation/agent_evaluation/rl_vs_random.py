import argparse

from evaluation.agent_evaluation.simulator import simulate
from evaluation.agents.random_agent import RandomAgent
from evaluation.agents.rl_agent import RLAgent
from evaluation.hand_calculation.tile_constants import EAST, SOUTH, WEST


def rl_vs_random(args):
    wind = args.wind
    discard_model_path = args.discard_model_path
    pon_model_path = args.pon_model_path
    kan_model_path = args.kan_model_path
    kita_model_path = args.kita_model_path
    riichi_model_path = args.riichi_model_path
    batch = args.batch

    rl_agent = RLAgent(
        wind=wind,
        discard_model_path=discard_model_path,
        pon_model_path=pon_model_path,
        kan_model_path=kan_model_path,
        kita_model_path=kita_model_path,
        riichi_model_path=riichi_model_path
    )

    if wind == EAST:
        players = [rl_agent, RandomAgent(), RandomAgent()]
    elif wind == SOUTH:
        players = [RandomAgent(), rl_agent, RandomAgent()]
    elif wind == WEST:
        players = [RandomAgent(), RandomAgent(), rl_agent]

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
    parser.add_argument('--wind', action='store', type=int, required=True)
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

    rl_vs_random(args)
