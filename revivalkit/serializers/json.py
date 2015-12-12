from __future__ import absolute_import

import json

in_text = True

def dump(x, f):
    return json.dump(x, f)

def load(f):
    return json.load(f)
