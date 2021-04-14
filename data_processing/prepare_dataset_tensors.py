import argparse
import os

import joblib
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split

from data_processing.data_processing_constants import DISCARD_COUNTS, \
    PON_COUNTS, KAN_COUNTS, KITA_COUNTS, RIICHI_COUNTS, DISCARD_MEAN, \
    DISCARD_STD, PON_MEAN, PON_STD, KAN_MEAN, KAN_STD, KITA_MEAN, KITA_STD, \
    RIICHI_MEAN, RIICHI_STD

assert tf.__version__ >= "2.0"

# To make the output stable across runs
np.random.seed(42)
tf.random.set_seed(42)

# Disable all GPUs
tf.config.set_visible_devices([], 'GPU')
visible_devices = tf.config.get_visible_devices()
for device in visible_devices:
    assert device.device_type != 'GPU'


def validate_dataset(dataset_path, action_type, year):
    if action_type == 'discard':
        path, dirs, files = next(
            os.walk(os.path.join(dataset_path, 'discard_' + year)))
        assert len(files) == DISCARD_COUNTS[year]

        with open(os.path.join(dataset_path,
                               'discard_actions_' + year + '.csv')) as f:
            f.readline()  # remove header
            assert sum(1 for line in f) == DISCARD_COUNTS[year]

    elif action_type == 'pon':
        path, dirs, files = next(
            os.walk(os.path.join(dataset_path, 'pon_' + year)))
        assert len(files) == PON_COUNTS[year]['total']

        with open(os.path.join(dataset_path,
                               'pon_actions_' + year + '.csv')) as f:
            f.readline()  # remove header
            assert sum(1 for line in f) == PON_COUNTS[year]['total']
            f.seek(0)
            f.readline()  # remove header
            assert sum(int(line[-2]) for line in f) == PON_COUNTS[year]['yes']

    elif action_type == 'kan':
        path, dirs, files = next(
            os.walk(os.path.join(dataset_path, 'kan_' + year)))
        assert len(files) == KAN_COUNTS[year]['total']

        with open(os.path.join(dataset_path,
                               'kan_actions_' + year + '.csv')) as f:
            f.readline()  # remove header
            assert sum(1 for line in f) == KAN_COUNTS[year]['total']
            f.seek(0)
            f.readline()  # remove header
            assert sum(int(line[-2]) for line in f) == KAN_COUNTS[year]['yes']

    elif action_type == 'kita':
        path, dirs, files = next(
            os.walk(os.path.join(dataset_path, 'kita_' + year)))
        assert len(files) == KITA_COUNTS[year]['total']

        with open(os.path.join(dataset_path,
                               'kita_actions_' + year + '.csv')) as f:
            f.readline()  # remove header
            assert sum(1 for line in f) == KITA_COUNTS[year]['total']
            f.seek(0)
            f.readline()  # remove header
            assert sum(int(line[-2]) for line in f) == KITA_COUNTS[year]['yes']

    else:  # action_type == 'riichi'
        path, dirs, files = next(
            os.walk(os.path.join(dataset_path, 'riichi_' + year)))
        assert len(files) == RIICHI_COUNTS[year]['total']

        with open(os.path.join(dataset_path,
                               'riichi_actions_' + year + '.csv')) as f:
            f.readline()  # remove header
            assert sum(1 for line in f) == RIICHI_COUNTS[year]['total']
            f.seek(0)
            f.readline()  # remove header
            assert sum(int(line[-2]) for line in f) == \
                   RIICHI_COUNTS[year]['yes']


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


def prepare_dataset_tensors(dataset_path, action_type, year, scaled=False):
    image_folder = action_type + '_' + year
    label_file = action_type + '_actions_' + year + '.csv'

    # # Only for the first time
    # validate_dataset(dataset_path, action_type, year)

    image_files = tf.data.Dataset.list_files(os.path.join(
        dataset_path, image_folder + '/*.png'))
    labels = load_csv(dataset_path, label_file)

    # # Only for the first time
    # for i in range(len(labels)):
    #     assert labels['image'][i] == action_type + '_' + year + '_' \
    #            + str(i + 1) + '.png'
    # print(action_type + ' dataset OK')
    # print()

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

    if scaled:
        X_mean = np.mean(X_train)
        X_std = np.std(X_train)
        if X_std == 0:
            X_std = 1e-7
        print(action_type + ' X_mean:', X_mean)
        print(action_type + ' X_std:', X_std)
        print()
        X_train = (X_train - X_mean) / X_std
        X_dev = (X_dev - X_mean) / X_std

    if scaled:
        filename = action_type + '_tensors_' + year + '_scaled'
    else:
        filename = action_type + '_tensors_' + year

    with open(os.path.join(dataset_path, filename + '.joblib'), 'wb') as fwrite:
        joblib.dump(X_train, fwrite)
        joblib.dump(X_dev, fwrite)
        joblib.dump(y_train, fwrite)
        joblib.dump(y_dev, fwrite)


def prepare_testset_tensors(dataset_path, action_type, year):
    image_folder = action_type + '_' + year
    label_file = action_type + '_actions_' + year + '.csv'

    # Only for the first time
    validate_dataset(dataset_path, action_type, year)

    image_files = tf.data.Dataset.list_files(os.path.join(
        dataset_path, image_folder + '/*.png'))
    labels = load_csv(dataset_path, label_file)

    # Only for the first time
    for i in range(len(labels)):
        assert labels['image'][i] == action_type + '_' + year + '_' \
               + str(i + 1) + '.png'
    print(action_type + ' dataset OK')
    print()

    # Generate (state, action) (i.e. (image, label)) pairs
    X = []
    y = []

    for file in image_files:
        image, label = generate_state_action_pair(file, labels, action_type,
                                                  year)
        X.append(image)
        y.append(label)

    X_test = tf.stack(X)
    y_test = tf.stack(y)
    print(action_type + ' X_test.shape:', X_test.shape)
    print(action_type + ' y_test.shape:', y_test.shape)
    print()

    if action_type == 'discard':
        X_test_scaled = (X_test - DISCARD_MEAN) / DISCARD_STD
    elif action_type == 'pon':
        X_test_scaled = (X_test - PON_MEAN) / PON_STD
    elif action_type == 'kan':
        X_test_scaled = (X_test - KAN_MEAN) / KAN_STD
    elif action_type == 'kita':
        X_test_scaled = (X_test - KITA_MEAN) / KITA_STD
    else:  # if action_type == 'riichi':
        X_test_scaled = (X_test - RIICHI_MEAN) / RIICHI_STD

    unscaled_filename = action_type + '_tensors_' + year + '.joblib'
    scaled_filename = action_type + '_tensors_' + year + '_scaled.joblib'

    with open(os.path.join(dataset_path, unscaled_filename), 'wb') as fwrite:
        joblib.dump(X_test, fwrite)
        joblib.dump(y_test, fwrite)

    with open(os.path.join(dataset_path, scaled_filename), 'wb') as fwrite:
        joblib.dump(X_test_scaled, fwrite)
        joblib.dump(y_test, fwrite)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset_path', action='store', type=str,
                        required=True)
    parser.add_argument('--action_type', action='store', type=str,
                        required=True)
    parser.add_argument('--year', action='store', type=str, required=True)
    parser.add_argument('--scaled', action='store', type=bool, required=False)

    args = parser.parse_args()
    dataset_path = args.dataset_path
    action_type = args.action_type
    year = args.year
    if args.scaled:
        scaled = args.scaled
    else:
        scaled = False

    # prepare_dataset_tensors(dataset_path, action_type, year, scaled)
    prepare_testset_tensors(dataset_path, action_type, year)

    print('Success')
