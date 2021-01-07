import argparse
import os
import pickle
from functools import partial

import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow import keras
from tqdm import tqdm

assert tf.__version__ >= "2.0"

# Parse the args
parser = argparse.ArgumentParser()
parser.add_argument('--dataset_path', action='store', type=str, required=True)
parser.add_argument('--cnn_path', action='store', type=str, required=True)

args = parser.parse_args()
dataset_path = args.dataset_path
cnn_path = args.cnn_path

# To make the output stable across runs
np.random.seed(42)
tf.random.set_seed(42)

TOTAL_FEATURES_COUNT = 12410
TOTAL_COLUMNS_SIZE = 365


def to_array(binary):
    return np.array([int(item) for item in
                     list(bin(binary)[2:].zfill(TOTAL_FEATURES_COUNT))]) \
        .reshape((34, TOTAL_COLUMNS_SIZE)).astype(float)


pon_data = pd.DataFrame(columns=['state', 'target'])

with tqdm(desc='Decoding', total=453590) as pbar:
    action_flag = False
    for i in range(20):
        filename = os.path.join(dataset_path,
                                'pon_2019_{:0>2d}'.format(i + 1) + '.pickle')
        with open(filename, 'rb') as fread:
            try:
                while True:
                    data = pickle.load(fread)
                    if action_flag:
                        target = to_array(data)
                        pon_data = pon_data.append(
                            {'state': state, 'target': target},
                            ignore_index=True)
                        pbar.update(1)
                    else:
                        state = to_array(data)
                    action_flag = not action_flag
            except EOFError:
                pass

X, y = np.stack(np.array(pon_data['state'])), pon_data['target']
X_train, X_dev, y_train, y_dev = train_test_split(X, y, test_size=0.1,
                                                  train_size=0.9,
                                                  random_state=42)
print('X_train shape:', X_train.shape)
print('X_dev.shape:', X_dev.shape)
print('y_train shape:', y_train.shape)
print('y_dev.shape:', y_dev.shape)

DefaultConv2D = partial(keras.layers.Conv2D, kernel_size=3, activation='relu',
                        padding="VALID")

tf.keras.backend.clear_session()

model = keras.models.Sequential([
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
    keras.layers.Dense(units=512, activation='relu'),
    keras.layers.BatchNormalization(),
    keras.layers.Dropout(0.5),
    keras.layers.Dense(units=2, activation='softmax'),
])

model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

history = model.fit(X_train, y_train, batch_size=32, epochs=500,
                    validation_data=(X_dev, y_dev))

with open(os.path.join(cnn_path, 'history.pickle'), 'wb') as f_history:
    pickle.dump(history, f_history)

model.save(os.path.join(cnn_path, 'pon_model.h5'))

eval_train = model.evaluate(X_train, y_train)
print('final training loss:', eval_train[0])
print('final training accuracy:', eval_train[1])
eval_dev = model.evaluate(X_dev, y_dev)
print('final dev loss:', eval_dev[0])
print('final dev accuracy:', eval_dev[1])
