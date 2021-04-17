import argparse
import os
from functools import partial

import joblib
import tensorflow as tf
from tensorflow import keras

assert tf.__version__ >= "2.0"

# To make the output stable across runs
tf.random.set_seed(42)


def load_data(dataset_path, filename):
    with open(os.path.join(dataset_path, filename), 'rb') as fread:
        X_test = joblib.load(fread)
        y_test = joblib.load(fread)

        return X_test, y_test


def create_model(action_type):
    if action_type == 'discard':
        DefaultConv2D = partial(keras.layers.Conv2D, kernel_size=[4, 5],
                                activation='relu', padding="VALID")

        return keras.models.Sequential([
            DefaultConv2D(filters=64, input_shape=[34, 366, 1]),
            keras.layers.BatchNormalization(),
            keras.layers.Dropout(0.5),

            DefaultConv2D(filters=64),
            keras.layers.BatchNormalization(),
            keras.layers.Dropout(0.5),

            DefaultConv2D(filters=64),
            keras.layers.BatchNormalization(),
            keras.layers.Dropout(0.5),

            DefaultConv2D(filters=32),
            keras.layers.BatchNormalization(),
            keras.layers.Dropout(0.5),

            keras.layers.Flatten(),

            keras.layers.Dense(units=256, activation='relu'),
            keras.layers.BatchNormalization(),
            keras.layers.Dropout(0.5),

            keras.layers.Dense(units=34, activation='softmax'),
        ])

    elif action_type == 'kita':
        DefaultConv2D = partial(keras.layers.Conv2D, kernel_size=[3, 2],
                                activation='relu', padding="VALID")

        return keras.models.Sequential([
            DefaultConv2D(filters=64, input_shape=[34, 366, 1]),
            keras.layers.BatchNormalization(),
            keras.layers.Dropout(0.5),

            DefaultConv2D(filters=64),
            keras.layers.BatchNormalization(),
            keras.layers.Dropout(0.5),

            DefaultConv2D(filters=64),
            keras.layers.BatchNormalization(),
            keras.layers.Dropout(0.5),

            DefaultConv2D(filters=32),
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
    parser.add_argument('--model_path', action='store', type=str, required=True)

    args = parser.parse_args()
    dataset_path = args.dataset_path
    logs_path = args.logs_path
    model_path = args.model_path

    # Test whether there are GPUs available
    assert len(tf.config.experimental.list_physical_devices('GPU')) > 0

    kernel_size = {
        'discard': '45',
        'pon': '54',
        'kan': '23',
        'kita': '32',
        'riichi': '34'
    }

    for action in 'discard', 'kita':
        for scaled in '', '_scaled':
            print('=================================================================')
            print(action + scaled + ' model evaluation')
            print('=================================================================')

            dataset_name = action + '_tensors_2020' + scaled + '.joblib'

            # Load dataset
            X_test, y_test = load_data(dataset_path, dataset_name)
            print(action + scaled, 'X_test shape:', X_test.shape)
            print(action + scaled, 'y_test.shape:', y_test.shape)
            print()

            # load model
            keras.backend.clear_session()

            model_name = action + '_cnn_' + kernel_size[action] + scaled
            checkpoint_dir = os.path.join(logs_path,
                                          model_name + '/checkpoints')
            model = create_model(action)
            model.load_weights(tf.train.latest_checkpoint(checkpoint_dir))

            # evaluation on test set
            model.compile(
                optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
                loss='sparse_categorical_crossentropy',
                metrics=['accuracy'])
            eval_test = model.evaluate(X_test, y_test)
            print(action + scaled, 'test loss:', eval_test[0])
            print(action + scaled, 'test accuracy:', eval_test[1])

            # save model
            model.save(os.path.join(model_path, model_name + '.h5'))
