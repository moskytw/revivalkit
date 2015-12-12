import sys
from os.path import abspath, dirname, join

try:
    # py2
    import cPickle as pickle
except ImportError:
    # py3
    import pickle

from . import log

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

def dump(x, f):
    return pickle.dump(x, f, pickle.HIGHEST_PROTOCOL)

def load(f):
    return pickle.load(f)

def encoffin(x, name=None):
    log.debug('encoffining', name, '...')
    with open(_to_coffin_path(name), 'wb') as f:
        return dump(x, f)

def decoffin(name=None):
    log.debug('decoffining', name, '...')
    with open(_to_coffin_path(name), 'rb') as f:
        return load(f)
