import tensorflow as tf

if __name__ == '__main__':
    gpus = tf.config.experimental.list_physical_devices('GPU')
    print(gpus)
