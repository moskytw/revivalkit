# Revival Kit

Let's revive from Ctrl-C or any exception!

![01_consume_queue.py_demo.gif](https://cloud.githubusercontent.com/assets/594141/11760658/916fd5aa-a0dd-11e5-8491-81dabca9f386.gif)

The code of [01_consume_queue.py](https://github.com/moskytw/revivalkit/blob/master/examples/01_consume_queue.py):

```python
from time import sleep
from revivalkit import revive

o = revive()
if not hasattr(o, 'que'):
    o.que = list(range(10))

print('current que: ', o.que)
while o.que:
    sleep(0.25)
    print('consumed', o.que.pop())
```

## Install via pip

```bash
pip install revivalkit
```

It supports both Python 2 and Python 3.

Thanks [uranusjr](https://github.com/uranusjr) and [ypsun](https://github.com/ypsun)'s help at [Taipei.py Projects On](http://www.meetup.com/Taipei-py/events/226558484/). :D

## Doc?

I'm still working on it. Please read the [examples](https://github.com/moskytw/revivalkit/blob/master/examples/) or just the source code.
