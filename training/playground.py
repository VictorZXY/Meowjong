import os
import numpy as np
import pandas as pd
import tensorflow as tf
from PIL import Image
from sklearn.model_selection import train_test_split
from tensorflow import keras

from data_processing.data_preprocessing_constants import DATASET_PATH

assert tf.__version__ >= "2.0"

# To make the output stable across runs
np.random.seed(42)
tf.random.set_seed(42)

PON_COUNT_2019 = {
    'total': 101020,
    'yes': 28462,
    'no': 72558
}
AUTOTUNE = tf.data.experimental.AUTOTUNE


def load_data(csv_file):
    csv_path = os.path.join(DATASET_PATH, csv_file)
    return pd.read_csv(csv_path, sep=',')


image_files = tf.data.Dataset.list_files(
    os.path.join(DATASET_PATH, 'pon_2019/*.png'))
labels = load_data('pon_actions_2019.csv')


def get_label(image_path):
    image_name = image_path.numpy().decode('utf-8').split('\\')[-1]
    image_index = int(image_name[9:-4])
    return tf.constant(labels['label'][image_index - 1])


def decode_image(image):
    image = tf.image.decode_png(image, channels=1)  # grayscale
    image = tf.image.convert_image_dtype(image, tf.float32)
    return image


def process_path(file_path):
    label = get_label(file_path)
    image = tf.io.read_file(file_path)
    image = decode_image(image)
    return image, label


if __name__ == '__main__':
    X, y = image_files.map(process_path, num_parallel_calls=AUTOTUNE)
    print(X)
    print(y)
