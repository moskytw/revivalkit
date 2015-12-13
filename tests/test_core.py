import pickle
import os
import shutil
import subprocess
import sys
import tempfile

import pytest


extra_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


REVIVE_SUBPROCESS_PROGRAM = ("""
import os
import sys

# Change cwd and script name to fool revivalkit for testing.
os.chdir(sys.argv[1])
sys.argv[0] = '___revive_subprocess'

sys.path.append(sys.argv[2])
from revivalkit import revive

o = revive()
if not getattr(o, 'queue', []):
    o.queue = ['james', 'harvey', 'oswald', 'bruce', 'selina']
while o.queue:
    n = o.queue.pop()
    if n == 'oswald':
        raise SystemExit(1)
    print(n)
""")


@pytest.fixture
def tempdir(request):
    dirname = tempfile.mkdtemp()

    def finalizer():
        shutil.rmtree(dirname)

    request.addfinalizer(finalizer)
    return dirname


@pytest.fixture
def revive_subprocess_args(tempdir):
    args = [
        sys.executable,
        '-c',
        REVIVE_SUBPROCESS_PROGRAM,
        tempdir,
        extra_path,
    ]
    return args


def test_revive(revive_subprocess_args):
    with pytest.raises(subprocess.CalledProcessError) as ctx:
        subprocess.check_output(revive_subprocess_args)
    assert ctx.value.returncode == 1
    assert ctx.value.output == b'selina\nbruce\n'

    my_coffin = os.path.join(
        revive_subprocess_args[3],
        '___revive_subprocess.coffin',
    )
    with open(my_coffin, 'rb') as f:
        o = pickle.load(f)
    assert o.queue == ['james', 'harvey']

    output = subprocess.check_output(revive_subprocess_args)
    assert output == b'harvey\njames\n'
