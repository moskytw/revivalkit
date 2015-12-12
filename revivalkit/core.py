from __future__ import print_function

import sys
from os.path import abspath, dirname, join
from functools import partial

from . import log
from . import before_exit
from . import serializers

# py2 raises IOError
# py3 raises OSError
# although py3 is backward compatible with IOError,
# we still rename it to write the py3-style code.
OSError = IOError

# path-related terms:
#
# path
# = dir_path/file_name
# = dir_path/base_name.ext
#

# main module's path
# we save the path here to avoid cwd changes
_main_mod_path = abspath(sys.argv[0])
_main_mod_dir_path = dirname(_main_mod_path)

ext = '.coffin'

def _add_ext(path):
    return path+ext

def _to_coffin_path(name):

    # if None, use main mod path
    if name is None:
        return _add_ext(_main_mod_path)

    # if it is a path, respect it
    if '.' in name or '/' in name:
        return name

    # auto
    return join(_main_mod_dir_path, _add_ext(name))

def _encoffin(serializer, x, name=None):
    log.debug('encoffining', name, '...')
    with open(
        _to_coffin_path(name),
        'wb'[:2-getattr(serializer, 'in_text', False)]
    ) as f:
        return serializer.dump(x, f)

def _decoffin(serializer, name=None):
    log.debug('decoffining', name, '...')
    with open(
        _to_coffin_path(name),
        'rb'[:2-getattr(serializer, 'in_text', False)]
    ) as f:
        return serializer.load(f)

class _Object(object):
    pass

def revive(make_default=None, name=None, serializer=None):

    if make_default is None:
        make_default = _Object

    if serializer is None:
        serializer = serializers.pickle

    try:
        x = _decoffin(serializer, name)
    except OSError:
        x = make_default()
        log.debug('uses default', name, x)

    before_exit.encoffining_que.append(
        partial(_encoffin, serializer, x, name)
    )
    log.debug('registered', name, x)

    return x

def append_cleanup(f):
    before_exit.cleanup_que.append(f)

if __name__ == '__main__':

    log.to_print_debug = True

    # revive o or set default
    o = revive()
    if not hasattr(o, 'que'):
        o.que = list(range(10))

    # register clean up
    def say_hi():
        print('hi!')
    append_cleanup(say_hi)

    # consume que
    from time import sleep
    print('current que: ', o.que)
    while o.que:
        sleep(0.25)
        print('consumed', o.que.pop())
