from __future__ import print_function

import sys

to_print_debug = False

def debug(*args, **arg_ds):
    if not to_print_debug:
        return
    print('revivalkit:debug:', *args, file=sys.stderr, **arg_ds)
