from __future__ import absolute_import

try:
    # py2
    import cPickle as pickle
except ImportError:
    # py3
    import pickle

def dump(x, filename):
    with open(filename, 'wb') as f:
        return pickle.dump(x, f, pickle.HIGHEST_PROTOCOL)

def load(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)
