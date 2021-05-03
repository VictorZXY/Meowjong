from tqdm import tqdm

from evaluation.agent_evaluation.simulator import simulate
from evaluation.agents.random_agent import RandomAgent


def random_vs_random():
    with open('..\\..\\results\\Random_vs_Random.txt', 'a') as fwrite:
        with tqdm(desc='Simulating', total=5000) as pbar:
            for i in range(5000):
                players = [RandomAgent(), RandomAgent(), RandomAgent()]
                round_scores = simulate(players, seed=i)
                fwrite.write(str(i) + ' '
                             + str(round_scores[0]) + ' '
                             + str(round_scores[1]) + ' '
                             + str(round_scores[2]) + ' \n')
                pbar.update(1)


if __name__ == '__main__':
    random_vs_random()
