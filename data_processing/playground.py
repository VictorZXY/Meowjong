import os
import numpy as np
import pandas as pd
import pickle

from tqdm import tqdm

from data_processing.data_preprocessing_constants import SELECTED_YEARS, \
    EXTRACTED_GAME_LOGS_PATH, GAME_LOGS_COUNT

if __name__ == '__main__':
    a = np.array([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]])
    a = a.reshape(10)
    print(a)
