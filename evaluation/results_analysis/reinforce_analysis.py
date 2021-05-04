import csv
import os

RESULTS_DIR = '..\\..\\results\\REINFORCE-evaluation\\'
CSV_FILENAME = '..\\..\\results\\REINFORCE-evaluation\\REINFORCE-evaluation.csv'
FIELD_NAMES = [
    'eps',
    'illegal_count',
    'east_win_rate',
    'south_win_rate',
    'west_win_rate',
    'total_win_rate',
    'east_loss_rate',
    'south_loss_rate',
    'west_loss_rate',
    'total_loss_rate',
    'east_avg_score',
    'south_avg_score',
    'west_avg_score',
    'total_avg_score'
]


class Lost(Exception):
    pass


if __name__ == '__main__':
    with open(CSV_FILENAME, 'w', newline='') as csvfile:
        csv_writer = csv.DictWriter(csvfile, fieldnames=FIELD_NAMES)
        csv_writer.writeheader()

        for eps in range(40):
            filename = str(eps + 1) + '.txt'
            # 0: East, 1: South, 2: West, 3: total
            win_scores = [[], [], [], []]
            loss_scores = [[], [], [], []]
            illegal_count = 0
            loss_count = 0

            with open(os.path.join(RESULTS_DIR, filename), 'r') as fread:
                for wind in range(3):
                    fread.readline()
                    for i in range(500):
                        line = fread.readline().strip().split()
                        if line[1] == 'ILLEGAL':
                            illegal_count += 1
                        else:
                            data = list(map(int, line))
                            if data[wind + 1] < 0:
                                loss_scores[wind].append(data[wind + 1])
                            elif data[wind + 1] > 0:
                                win_scores[wind].append(data[wind + 1])

            csv_writer.writerow({
                'eps': (eps + 1) * 10,
                'illegal_count': illegal_count,
                'east_win_rate': len(win_scores[0]) / (500 - illegal_count),
                'south_win_rate': len(win_scores[1]) / (500 - illegal_count),
                'west_win_rate': len(win_scores[2]) / (500 - illegal_count),
                'total_win_rate': (len(win_scores[0]) + len(win_scores[1]) + len(win_scores[2])) / (1500 - 3 * illegal_count),
                'east_loss_rate': len(loss_scores[0]) / (500 - illegal_count),
                'south_loss_rate': len(loss_scores[1]) / (500 - illegal_count),
                'west_loss_rate': len(loss_scores[2]) / (500 - illegal_count),
                'total_loss_rate': (len(loss_scores[0]) + len(loss_scores[1]) + len(loss_scores[2])) / (1500 - 3 * illegal_count),
                'east_avg_score': (sum(win_scores[0]) + sum(loss_scores[0])) / (len(win_scores[0]) + len(loss_scores[0])),
                'south_avg_score': (sum(win_scores[1]) + sum(loss_scores[1])) / (len(win_scores[1]) + len(loss_scores[1])),
                'west_avg_score': (sum(win_scores[2]) + sum(loss_scores[2])) / (len(win_scores[2]) + len(loss_scores[2])),
                'total_avg_score': (sum(win_scores[0]) + sum(win_scores[1]) + sum(win_scores[2]) + sum(loss_scores[0]) + sum(loss_scores[1]) + sum(loss_scores[2]))
                                   / (len(win_scores[0]) + len(win_scores[1]) + len(win_scores[2]) + len(loss_scores[0]) + len(loss_scores[1]) + len(loss_scores[2]))
            })
