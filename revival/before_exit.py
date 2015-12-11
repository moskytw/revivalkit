from __future__ import print_function

import sys
import atexit
import signal
from collections import deque

from revival import log

message = 'still cleaning up ...'

def _print_still_saving(signum, frame):
    print('{}:'.format(sys.argv[0]), message, file=sys.stderr)

_orig_sigint_handler = signal.getsignal(signal.SIGINT)

def _mute_sigint():
    _orig_sigint_handler = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, _print_still_saving)
    log.debug('muted sigint')

def _restore_sigint():
    signal.signal(signal.SIGINT, _orig_sigint_handler)
    log.debug('restored sigint')

class _Queue(deque):

    def execute_all(self):
        for f in self:
            log.debug('calling', f, '...')
            f()
            log.debug('called', f)

encoffining_que = _Queue()
cleanup_que = _Queue()

# if you register A, B, and C, at interpreter termination time they will be run
# in the order C, B, A. -- https://docs.python.org/3.5/library/atexit.html
atexit.register(_restore_sigint)
atexit.register(encoffining_que.execute_all)
atexit.register(cleanup_que.execute_all)
atexit.register(_mute_sigint)
