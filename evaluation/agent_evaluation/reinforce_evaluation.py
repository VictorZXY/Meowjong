import argparse

from evaluation.agent_evaluation.simulator import simulate
from evaluation.agents.random_agent import RandomAgent
from evaluation.agents.rl_agent import RLAgent
from evaluation.hand_calculation.tile_constants import EAST, SOUTH, WEST


def reinforce_evaluation(args):
    discard_model_path = args.discard_model_path
    pon_model_path = args.pon_model_path
    kan_model_path = args.kan_model_path
    kita_model_path = args.kita_model_path
    riichi_model_path = args.riichi_model_path

    rl_agent = RLAgent(
        wind=EAST,
        discard_model_path=discard_model_path,
        pon_model_path=pon_model_path,
        kan_model_path=kan_model_path,
        kita_model_path=kita_model_path,
        riichi_model_path=riichi_model_path
    )

    for wind in EAST, SOUTH, WEST:
        if wind == EAST:
            print('wind = East:')
            players = [rl_agent, RandomAgent(), RandomAgent()]
        elif wind == SOUTH:
            print('wind = South:')
            players = [RandomAgent(), rl_agent, RandomAgent()]
        else:  # if wind == WEST:
            print('wind = West:')
            players = [RandomAgent(), RandomAgent(), rl_agent]

        for i in range(500):
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

    reinforce_evaluation(args)
