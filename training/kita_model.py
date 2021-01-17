import argparse
import os
import pickle
from datetime import datetime
from functools import partial

import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow import keras

assert tf.__version__ >= "2.0"

# To make the output stable across runs
np.random.seed(42)
tf.random.set_seed(42)

AUTOTUNE = tf.data.experimental.AUTOTUNE
BATCH_SIZE_PER_REPLICA = 32

TOTAL_FEATURES_COUNT = 12410
TOTAL_COLUMNS_SIZE = 365
KITA_COUNT_2019 = {
    'total': 90866,
    'yes': 76582,
    'no': 14284
}


def kernel(arg):
    try:
        x, y = map(int, arg.split(','))
        return x, y
    except Exception:
        raise argparse.ArgumentTypeError("Kernel size must be x, y")


def validate_dataset(dataset_path):
    path, dirs, files = next(os.walk(os.path.join(dataset_path, 'kita_2019')))
    assert len(files) == KITA_COUNT_2019['total']

    with open(os.path.join(dataset_path, 'kita_actions_2019.csv')) as f:
        f.readline()
        assert sum(1 for line in f) == KITA_COUNT_2019['total']
        f.seek(0)
        f.readline()
        assert sum(int(line[-2]) for line in f) == KITA_COUNT_2019['yes']


def load_data(csv_file):
    csv_path = os.path.join(dataset_path, csv_file)
    return pd.read_csv(csv_path, sep=',')


def get_label(image_file, labels):
    # image_name = image_file.numpy().decode('utf-8').split('\\')[-1]  # Windows
    image_name = image_file.numpy().decode('utf-8').split('/')[-1]  # Linux
    image_index = int(image_name[10:-4])
    return tf.constant(labels['label'][image_index - 1])


def decode_image(image):
    image = tf.image.decode_png(image, channels=1)  # grayscale
    image = tf.image.convert_image_dtype(image, tf.float32)
    return image


def generate_state_action_pair(image_file, labels):
    label = get_label(image_file, labels)
    image = tf.io.read_file(image_file)
    image = decode_image(image)
    return image, label


def create_model(kernel_size):
    DefaultConv2D = partial(keras.layers.Conv2D, kernel_size=kernel_size,
                            activation='relu',
                            padding="VALID")
    return keras.models.Sequential([
        DefaultConv2D(filters=128, input_shape=[34, 365, 1]),
        keras.layers.BatchNormalization(),
        keras.layers.Dropout(0.5),
        DefaultConv2D(filters=128),
        keras.layers.BatchNormalization(),
        keras.layers.Dropout(0.5),
        DefaultConv2D(filters=128),
        keras.layers.BatchNormalization(),
        keras.layers.Dropout(0.5),
        keras.layers.Flatten(),
        keras.layers.Dense(units=512, activation='relu'),
        keras.layers.BatchNormalization(),
        keras.layers.Dropout(0.5),
        keras.layers.Dense(units=256, activation='relu'),
        keras.layers.BatchNormalization(),
        keras.layers.Dropout(0.5),
        keras.layers.Dense(units=2, activation='softmax'),
    ])


if __name__ == '__main__':
    # Parse the args
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset_path', action='store', type=str,
                        required=True)
    parser.add_argument('--logs_path', action='store', type=str, required=True)
    parser.add_argument('--cnn_path', action='store', type=str, required=True)
    parser.add_argument('--kernel_size', action='store', type=kernel,
                        required=True)

    args = parser.parse_args()
    dataset_path = args.dataset_path
    logs_path = args.logs_path
    cnn_path = args.cnn_path
    kernel_size = args.kernel_size

    # Load and validate the dataset
    validate_dataset(dataset_path)

    image_files = tf.data.Dataset.list_files(os.path.join(dataset_path,
                                                          'kita_2019/*.png'))
    labels = load_data('kita_actions_2019.csv')
    for i in range(len(labels)):
        assert labels['image'][i] == 'kita_2019_' + str(i + 1) + '.png'
    print('Dataset OK')
    print()

    # Generate (state, action) (i.e. (image, label)) pairs
    X = []
    y = []

    for file in image_files:
        image, label = generate_state_action_pair(file, labels)
        X.append(image)
        y.append(label)

    X_train, X_dev, y_train, y_dev = train_test_split(X, y, test_size=0.1,
                                                      train_size=0.9,
                                                      random_state=42,
                                                      stratify=y)
    X_train = tf.stack(X_train)
    X_dev = tf.stack(X_dev)
    y_train = tf.stack(y_train)
    y_dev = tf.stack(y_dev)
    print('X_train shape:', X_train.shape)
    print('X_dev.shape:', X_dev.shape)
    print('y_train shape:', y_train.shape)
    print('y_dev.shape:', y_dev.shape)
    print()

    # Create neural network
    assert len(tf.config.experimental.list_physical_devices('GPU')) > 0
    tf.keras.backend.clear_session()

    strategy = tf.distribute.MirroredStrategy()
    num_of_gpus = strategy.num_replicas_in_sync
    print('Number of devices:', num_of_gpus)
    print()

    with strategy.scope():
        model = create_model(kernel_size)
        model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
                      loss='sparse_categorical_crossentropy',
                      metrics=['accuracy'])
        print(model.summary())
        print()

    # Train the neural network
    model_name = 'kita_cnn_' + str(kernel_size[0]) + str(kernel_size[1])
    log_dir = os.path.join(logs_path + '/' + model_name + '/tensorboard_logs',
                           datetime.now().strftime("%Y%m%d-%H%M%S"))
    checkpoint_prefix = os.path.join(logs_path + '/' + model_name
                                     + '/training_checkpoints',
                                     "checkpoint_{epoch}")

    callbacks = [
        tf.keras.callbacks.TensorBoard(log_dir=log_dir),
        tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_prefix,
                                           save_weights_only=True)
    ]

    BATCH_SIZE = BATCH_SIZE_PER_REPLICA * num_of_gpus
    history = model.fit(X_train, y_train, batch_size=BATCH_SIZE, epochs=500,
                        validation_data=(X_dev, y_dev),
                        callbacks=callbacks)

    # Save the neural network
    with open(os.path.join(cnn_path + '/' + model_name,
                           model_name + '_history.pickle'), 'wb') \
            as f_history:
        pickle.dump(history, f_history)

    model.save(os.path.join(cnn_path + '/' + model_name, model_name + '.h5'))

    eval_train = model.evaluate(X_train, y_train)
    print('final training loss:', eval_train[0])
    print('final training accuracy:', eval_train[1])
    eval_dev = model.evaluate(X_dev, y_dev)
    print('final dev loss:', eval_dev[0])
    print('final dev accuracy:', eval_dev[1])
