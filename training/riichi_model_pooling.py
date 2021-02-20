import argparse
import os
import pickle
from datetime import datetime
from functools import partial

import tensorflow as tf
from tensorflow import keras

assert tf.__version__ >= "2.0"

# To make the output stable across runs
tf.random.set_seed(42)

AUTOTUNE = tf.data.experimental.AUTOTUNE
BATCH_SIZE_PER_REPLICA = 32

TOTAL_FEATURES_COUNT = 12410
TOTAL_COLUMNS_SIZE = 365


def kernel(arg):
    try:
        x, y = map(int, arg.split(','))
        return x, y
    except Exception:
        raise argparse.ArgumentTypeError("Kernel size must be x, y")


def load_data(dataset_path, filename):
    with open(os.path.join(dataset_path, filename), 'rb') as fread:
        X_train = pickle.load(fread)
        X_dev = pickle.load(fread)
        y_train = pickle.load(fread)
        y_dev = pickle.load(fread)

        return X_train, X_dev, y_train, y_dev


def create_model(kernel_size):
    DefaultConv2D = partial(keras.layers.Conv2D, kernel_size=kernel_size,
                            activation='relu',
                            padding="VALID")

    return keras.models.Sequential([
        DefaultConv2D(filters=64, input_shape=[34, 365, 1]),
        keras.layers.AvgPool2D(pool_size=2),
        keras.layers.BatchNormalization(),
        keras.layers.Dropout(0.5),

        DefaultConv2D(filters=64),
        keras.layers.AvgPool2D(pool_size=2),
        keras.layers.BatchNormalization(),
        keras.layers.Dropout(0.5),

        DefaultConv2D(filters=64),
        keras.layers.AvgPool2D(pool_size=2),
        keras.layers.BatchNormalization(),
        keras.layers.Dropout(0.5),

        DefaultConv2D(filters=32),
        keras.layers.AvgPool2D(pool_size=2),
        keras.layers.BatchNormalization(),
        keras.layers.Dropout(0.5),

        keras.layers.Flatten(),

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

    # Test whether there are GPUs available
    assert len(tf.config.experimental.list_physical_devices('GPU')) > 0

    # Load the dataset
    X_train, X_dev, y_train, y_dev = load_data(dataset_path,
                                               'riichi_tensors_2019.pickle')
    print('X_train shape:', X_train.shape)
    print('X_dev.shape:', X_dev.shape)
    print('y_train shape:', y_train.shape)
    print('y_dev.shape:', y_dev.shape)
    print()

    # Create neural network
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
    model_name = 'riichi_cnn_' + str(kernel_size[0]) + str(kernel_size[1])
    log_dir = os.path.join(logs_path + '/' + model_name + '/tensorboard_logs',
                           datetime.now().strftime("%Y%m%d-%H%M%S"))
    checkpoint_prefix = os.path.join(logs_path + '/' + model_name
                                     + '/training_checkpoints',
                                     "checkpoint_{epoch}")

    callbacks = [
        tf.keras.callbacks.TensorBoard(log_dir=log_dir),
        tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_prefix,
                                           save_best_only=True,
                                           save_weights_only=True,
                                           period=10)
    ]

    BATCH_SIZE = BATCH_SIZE_PER_REPLICA * num_of_gpus
    history = model.fit(X_train, y_train, batch_size=BATCH_SIZE, epochs=600,
                        validation_data=(X_dev, y_dev),
                        callbacks=callbacks)

    # Save the neural network
    model.save(os.path.join(cnn_path, model_name + '.h5'))

    eval_train = model.evaluate(X_train, y_train)
    print('final training loss:', eval_train[0])
    print('final training accuracy:', eval_train[1])
    eval_dev = model.evaluate(X_dev, y_dev)
    print('final dev loss:', eval_dev[0])
    print('final dev accuracy:', eval_dev[1])
