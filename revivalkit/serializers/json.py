from __future__ import absolute_import

import json


def dump(x, filename):
    with open(filename, 'w') as f:
        return json.dump(x, f)


def load(filename):
    with open(filename) as f:
        return json.load(f)
