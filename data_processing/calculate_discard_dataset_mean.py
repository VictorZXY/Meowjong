import argparse
import os

import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split

assert tf.__version__ >= "2.0"

# To make the output stable across runs
np.random.seed(42)
tf.random.set_seed(42)

# Disable all GPUs
tf.config.set_visible_devices([], 'GPU')
visible_devices = tf.config.get_visible_devices()
for device in visible_devices:
    assert device.device_type != 'GPU'


def load_csv(dataset_path, csv_file):
    csv_path = os.path.join(dataset_path, csv_file)
    return pd.read_csv(csv_path, sep=',')


def get_label(image_file, labels, action_type, year):
    # image_name = image_file.numpy().decode('utf-8').split('\\')[-1]  # Windows
    image_name = image_file.numpy().decode('utf-8').split('/')[-1]  # Linux

    image_file_prefix = action_type + '_' + year + '_'
    image_file_prefix_len = len(image_file_prefix)
    image_file_extension = '.png'
    image_file_extension_len = len(image_file_extension)

    image_index = int(image_name[image_file_prefix_len:
                                 -image_file_extension_len])
    return tf.constant(labels['label'][image_index - 1])


def decode_image(image):
    image = tf.image.decode_png(image, channels=1)  # grayscale
    image = tf.image.convert_image_dtype(image, tf.float32)
    return image


def generate_state_action_pair(image_file, labels, action_type, year):
    label = get_label(image_file, labels, action_type, year)
    image = tf.io.read_file(image_file)
    image = decode_image(image)
    return image, label


def calculate_discard_dataset_mean(dataset_path, action_type, year):
    image_folder = action_type + '_' + year
    label_file = action_type + '_actions_' + year + '.csv'

    image_files = tf.data.Dataset.list_files(os.path.join(
        dataset_path, image_folder + '/*.png'))
    labels = load_csv(dataset_path, label_file)

    # Generate (state, action) (i.e. (image, label)) pairs
    X = []
    y = []

    for file in image_files:
        image, label = generate_state_action_pair(file, labels, action_type,
                                                  year)
        X.append(image)
        y.append(label)

    X_train, X_dev, y_train, y_dev = train_test_split(X, y,
                                                      test_size=0.1,
                                                      train_size=0.9,
                                                      random_state=42,
                                                      stratify=y)
    X_train = tf.stack(X_train)
    X_dev = tf.stack(X_dev)
    y_train = tf.stack(y_train)
    y_dev = tf.stack(y_dev)
    print(action_type + ' X_train.shape:', X_train.shape)
    print(action_type + ' X_dev.shape:', X_dev.shape)
    print(action_type + ' y_train.shape:', y_train.shape)
    print(action_type + ' y_dev.shape:', y_dev.shape)
    print()

    X_mean = np.mean(X_train)
    print(action_type + ' X_mean:', X_mean)
    print()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset_path', action='store', type=str,
                        required=True)
    parser.add_argument('--action_type', action='store', type=str,
                        required=True)
    parser.add_argument('--year', action='store', type=str, required=True)

    args = parser.parse_args()
    dataset_path = args.dataset_path
    action_type = args.action_type
    year = args.year

    calculate_discard_dataset_mean(dataset_path, action_type, year)

    print('Success')
