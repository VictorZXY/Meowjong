import os
from collections import deque

import numpy as np
import pandas as pd
import pickle
from itertools import product

from pyswip import Prolog
from tqdm import tqdm

from data_processing.data_preprocessing_constants import SELECTED_YEARS, \
    EXTRACTED_GAME_LOGS_PATH, GAME_LOGS_COUNT, DATASET_PATH
from data_processing.prepare_dataset import encode_game_log

if __name__ == '__main__':
    print(type(None) is int)
