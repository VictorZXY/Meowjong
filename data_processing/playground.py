import numpy as np

from data_processing.data_preprocessing_constants import TOTAL_FEATURES_COUNT


def connect_bit(x, y):
    return (x << 1) | y


connect_bit = np.frompyfunc(connect_bit, 2, 1)

if __name__ == '__main__':
    a = np.ones(TOTAL_FEATURES_COUNT, dtype='int')
    print(connect_bit.reduce(a))
