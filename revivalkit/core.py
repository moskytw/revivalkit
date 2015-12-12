from __future__ import print_function

from functools import partial

from . import log
from . import before_exit
from . import utils

# py3 style
OSError = IOError

class _Object(object):
    pass

def revive(make_default=None, name=None):

    if make_default is None:
        make_default = _Object

    try:
        x = utils.decoffin(name)
    except OSError:
        x = make_default()
        log.debug('uses default', name, x)

    before_exit.encoffining_que.append(
        partial(utils.encoffin, x, name)
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
