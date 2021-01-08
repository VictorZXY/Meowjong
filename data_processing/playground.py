import numpy as np

from data_processing.data_preprocessing_constants import TOTAL_FEATURES_COUNT


def connect_bit(x, y):
    return (x << 1) | y


connect_bit = np.frompyfunc(connect_bit, 2, 1)

if __name__ == '__main__':
    a = np.array([
        [1, 1, 0, 0],
        [1, 0, 0, 0],
        [1, 1, 1, 0],
        [0, 0, 0, 0],
        [1, 0, 1, 0],
        [0, 1, 1, 1]
    ])
    print(a.shape)
    print(np.sum(a, axis=1).tolist())
