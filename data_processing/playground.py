import numpy as np

from data_processing.data_preprocessing_constants import TOTAL_FEATURES_COUNT


def foo(a, b, c):
    a += 1
    b['b'] += 1
    c['c'] += 1
    return a


if __name__ == '__main__':
    a = 0
    b = {
        'a': 0, 'b': 0, 'c': 0
    }
    c = {
        'a': 0, 'b': 0, 'c': 0
    }
    a = foo(a, b, c)
    a = foo(a, b, c)
    print(a)
    print(b)
    print(c)
