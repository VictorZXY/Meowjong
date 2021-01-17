import tensorflow as tf

if __name__ == '__main__':
    devices = tf.config.experimental.list_physical_devices()
    print(devices)
