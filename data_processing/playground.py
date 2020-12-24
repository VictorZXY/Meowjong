import os
from collections import deque

import numpy as np
import pandas as pd
import pickle
from itertools import product

from pyswip import Prolog
from tqdm import tqdm

from data_processing.data_preprocessing_constants import SELECTED_YEARS, \
    EXTRACTED_GAME_LOGS_PATH, GAME_LOGS_COUNT, DATASET_PATH, \
    TOTAL_FEATURES_COUNT
from data_processing.prepare_dataset import encode_game_log

def connect_bit(x, y):
    return (x << 1) | y

connect_bit = np.frompyfunc(connect_bit, 2, 1)

if __name__ == '__main__':
    a = np.ones(TOTAL_FEATURES_COUNT, dtype='int')
    print(connect_bit.reduce(a))
