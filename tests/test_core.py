import pickle
import os
import shutil
import subprocess
import sys
import tempfile

import pytest


EXTRA_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture
def tempdir(request):
    dirname = tempfile.mkdtemp()

    def finalizer():
        shutil.rmtree(dirname)

    request.addfinalizer(finalizer)
    return dirname


DEFAULT_PROGRAM_TEMPLATE = """
import os
import sys

# Change cwd and script name to fool revivalkit for testing.
os.chdir(sys.argv[1])
sys.argv[0] = '___revive_subprocess'

sys.path.append(sys.argv[2])
from revivalkit import revive

o = revive({revive_code})
if not getattr(o, 'queue', []):
    o.queue = ['james', 'harvey', 'oswald', 'bruce', 'selina']
while o.queue:
    n = o.queue.pop()
    if n == 'oswald':
        raise SystemExit(1)
    print(n)
"""

@pytest.mark.parametrize('revive_code, coffin_name', [
    ('', '___revive_subprocess.coffin'),
    ("name='my'", 'my.coffin'),
    ("name='mycoffin.pickle'", 'mycoffin.pickle'),
])
def test_revive(tempdir, revive_code, coffin_name):
    subprocess_args = [
        sys.executable, '-c',
        DEFAULT_PROGRAM_TEMPLATE.format(revive_code=revive_code),
        tempdir, EXTRA_PATH,
    ]
    with pytest.raises(subprocess.CalledProcessError) as ctx:
        subprocess.check_output(subprocess_args)
    assert ctx.value.returncode == 1
    assert ctx.value.output == b'selina\nbruce\n'

    with open(os.path.join(tempdir, coffin_name), 'rb') as f:
        o = pickle.load(f)
    assert o.queue == ['james', 'harvey']

    output = subprocess.check_output(subprocess_args)
    assert output == b'harvey\njames\n'


JSON_PROGRAM_TEMPLATE = """
import json
import os
import sys

# Change cwd and script name to fool revivalkit for testing.
os.chdir(sys.argv[1])
sys.argv[0] = '___revive_subprocess'

sys.path.append(sys.argv[2])
from revivalkit import revive

{serializer_code}

queue = revive({revive_code})
if not queue:
    queue.extend(['james', 'harvey', 'oswald', 'bruce', 'selina'])
while queue:
    n = queue.pop()
    if n == 'oswald':
        raise SystemExit(1)
    print(n)
"""

JSON_SERIALIZER_CODE = """
class JSONSerializer(object):
    IN_TEXT = True
    load = staticmethod(json.load)
    dump = staticmethod(json.dump)
"""

@pytest.mark.parametrize('format_params', [
    {'serializer_code': '',
     'revive_code': 'make_default=list, serializer=json, in_text=True'},
    {'serializer_code': JSON_SERIALIZER_CODE,
     'revive_code': 'make_default=list, serializer=JSONSerializer'},
])
def test_revive_json(tempdir, format_params):
    """Test two variants of the "in-text" hint feature.

    The JSON_PROGRAM variant uses the built-in ``json`` module as the
    serializer, and supply the ``in_text`` argument to ``revive`` manually.
    The JSON_SERIALIZER_PROGRAM wraps ``json`` in a thin wrapper with
    an ``IN_TEXT`` flag. This eliminates the ``in_text`` hint when
    calling ``revive``.
    """
    subprocess_args = [
        sys.executable, '-c',
        JSON_PROGRAM_TEMPLATE.format(**format_params),
        tempdir,
        EXTRA_PATH,
    ]
    with pytest.raises(subprocess.CalledProcessError) as ctx:
        subprocess.check_output(subprocess_args)
    assert ctx.value.returncode == 1
    assert ctx.value.output == b'selina\nbruce\n'

    with open(os.path.join(tempdir, '___revive_subprocess.coffin')) as f:
        assert f.read() == '["james", "harvey"]'

    output = subprocess.check_output(subprocess_args)
    assert output == b'harvey\njames\n'
