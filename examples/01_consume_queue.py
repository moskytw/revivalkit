from __future__ import print_function
from time import sleep
from revival import revive

o = revive()
if not hasattr(o, 'que'):
    o.que = list(range(10))

print('current que: ', o.que)
while o.que:
    sleep(0.25)
    print('consumed', o.que.pop())
