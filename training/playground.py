import os
import pickle
import numpy as np

from PIL import Image

from data_processing.data_preprocessing_constants import TOTAL_FEATURES_COUNT, \
    TOTAL_COLUMNS_SIZE


def to_array(binary):
    return np.array([int(item) for item in
                     list(bin(binary)[2:].zfill(TOTAL_FEATURES_COUNT))]) \
        .reshape((34, TOTAL_COLUMNS_SIZE)).astype(np.uint8) * 255


if __name__ == '__main__':
    print('Hello World!')
