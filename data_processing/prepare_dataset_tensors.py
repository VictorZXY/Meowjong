import argparse
import os
import joblib
import pickle

import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split

assert tf.__version__ >= "2.0"

# To make the output stable across runs
tf.random.set_seed(42)

DISCARD_COUNT_2019 = 885873
PON_COUNT_2019 = {
    'total': 101020,
    'yes': 28462,
    'no': 72558
}
KAN_COUNT_2019 = {
    'total': 148186,
    'yes': 3459,
    'no': 144727
}
KITA_COUNT_2019 = {
    'total': 90866,
    'yes': 76582,
    'no': 14284
}
RIICHI_COUNT_2019 = {
    'total': 74411,
    'yes': 21860,
    'no': 52551
}


def validate_dataset(dataset_path, action_type):
    if action_type == 'discard':
        path, dirs, files = next(
            os.walk(os.path.join(dataset_path, 'discard_2019')))
        assert len(files) == DISCARD_COUNT_2019

        with open(os.path.join(dataset_path, 'discard_actions_2019.csv')) as f:
            f.readline()
            assert sum(1 for line in f) == DISCARD_COUNT_2019

    elif action_type == 'pon':
        path, dirs, files = next(
            os.walk(os.path.join(dataset_path, 'pon_2019')))
        assert len(files) == PON_COUNT_2019['total']

        with open(os.path.join(dataset_path, 'pon_actions_2019.csv')) as f:
            f.readline()
            assert sum(1 for line in f) == PON_COUNT_2019['total']
            f.seek(0)
            f.readline()
            assert sum(int(line[-2]) for line in f) == PON_COUNT_2019['yes']

    elif action_type == 'kan':
        path, dirs, files = next(
            os.walk(os.path.join(dataset_path, 'kan_2019')))
        assert len(files) == KAN_COUNT_2019['total']

        with open(os.path.join(dataset_path, 'kan_actions_2019.csv')) as f:
            f.readline()
            assert sum(1 for line in f) == KAN_COUNT_2019['total']
            f.seek(0)
            f.readline()
            assert sum(int(line[-2]) for line in f) == KAN_COUNT_2019['yes']

    elif action_type == 'kita':
        path, dirs, files = next(
            os.walk(os.path.join(dataset_path, 'kita_2019')))
        assert len(files) == KITA_COUNT_2019['total']

        with open(os.path.join(dataset_path, 'kita_actions_2019.csv')) as f:
            f.readline()
            assert sum(1 for line in f) == KITA_COUNT_2019['total']
            f.seek(0)
            f.readline()
            assert sum(int(line[-2]) for line in f) == KITA_COUNT_2019['yes']

    else:  # action_type == 'riichi'
        path, dirs, files = next(
            os.walk(os.path.join(dataset_path, 'riichi_2019')))
        assert len(files) == RIICHI_COUNT_2019['total']

        with open(os.path.join(dataset_path, 'riichi_actions_2019.csv')) as f:
            f.readline()
            assert sum(1 for line in f) == RIICHI_COUNT_2019['total']
            f.seek(0)
            f.readline()
            assert sum(int(line[-2]) for line in f) == RIICHI_COUNT_2019['yes']


def load_csv(dataset_path, csv_file):
    csv_path = os.path.join(dataset_path, csv_file)
    return pd.read_csv(csv_path, sep=',')


def get_label(image_file, labels, action_type):
    # image_name = image_file.numpy().decode('utf-8').split('\\')[-1]  # Windows
    image_name = image_file.numpy().decode('utf-8').split('/')[-1]  # Linux

    image_file_prefix = action_type + '_2019_'
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


def generate_state_action_pair(image_file, labels, action_type):
    label = get_label(image_file, labels, action_type)
    image = tf.io.read_file(image_file)
    image = decode_image(image)
    return image, label


def prepare_dataset_tesnors(dataset_path, action_type, scaled=False):
    image_folder = action_type + '_2019'
    label_file = action_type + '_actions_2019.csv'

    # validate_dataset(dataset_path, action_type)

    image_files = tf.data.Dataset.list_files(os.path.join(
        dataset_path, image_folder + '/*.png'))
    labels = load_csv(dataset_path, label_file)
    for i in range(len(labels)):
        assert labels['image'][i] == action_type + \
               '_2019_' + str(i + 1) + '.png'
    print(action_type + ' dataset OK')
    print()

    # Generate (state, action) (i.e. (image, label)) pairs
    X = []
    y = []

    for file in image_files:
        image, label = generate_state_action_pair(file, labels, action_type)
        X.append(image)
        y.append(label)

    X_train, X_dev, y_train, y_dev = train_test_split(X, y, test_size=0.1,
                                                      train_size=0.9,
                                                      random_state=42,
                                                      stratify=y)

    if scaled:
        X_mean = np.mean(X_train, axis=0, keepdims=True)
        X_std = np.std(X_train, axis=0, keepdims=True) + 1e-7
        X_train = (X_train - X_mean) / X_std
        X_dev = (X_dev - X_mean) / X_std

    X_train = tf.stack(X_train)
    X_dev = tf.stack(X_dev)
    y_train = tf.stack(y_train)
    y_dev = tf.stack(y_dev)

    if scaled:
        filename = action_type + '_tensors_2019_scaled'
    else:
        filename = action_type + '_tensors_2019'

    if action_type == 'discard':
        with open(os.path.join(dataset_path, filename + '.joblib'), 'wb') \
                as fwrite:
            joblib.dump(X_train, fwrite)
            joblib.dump(X_dev, fwrite)
            joblib.dump(y_train, fwrite)
            joblib.dump(y_dev, fwrite)
    else:
        with open(os.path.join(dataset_path, filename + '.pickle'), 'wb') \
                as fwrite:
            pickle.dump(X_train, fwrite)
            pickle.dump(X_dev, fwrite)
            pickle.dump(y_train, fwrite)
            pickle.dump(y_dev, fwrite)

    print(action_type + ' X_train shape:', X_train.shape)
    print(action_type + ' X_dev.shape:', X_dev.shape)
    print(action_type + ' y_train shape:', y_train.shape)
    print(action_type + ' y_dev.shape:', y_dev.shape)
    print()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset_path', action='store', type=str,
                        required=True)
    parser.add_argument('--action_type', action='store', type=str,
                        required=True)
    parser.add_argument('--scaled', action='store', type=bool, required=False)

    args = parser.parse_args()
    dataset_path = args.dataset_path
    action_type = args.action_type
    if args.scaled:
        scaled = args.scaled
    else:
        scaled = False

    prepare_dataset_tesnors(dataset_path, action_type, scaled)

    print('Success')
