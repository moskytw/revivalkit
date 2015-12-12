from __future__ import absolute_import

import json

def dump(x, f):
    return json.dump(x, f)

def load(f):
    return json.load(f)
