import os
import numpy as np
import pandas as pd
import pickle

from tqdm import tqdm

from data_processing.data_preprocessing_constants import SELECTED_YEARS, \
    EXTRACTED_GAME_LOGS_PATH, GAME_LOGS_COUNT
from data_processing.prepare_dataset import to_binary, to_array

if __name__ == '__main__':
    r = 0
    for i in range(34 * 364):
        r = (r << 1) + 1
    print(r)
    a = np.ones((34, 364))
    b = to_binary(a)
    print(b)
    c = to_array(b)
    print(c)
