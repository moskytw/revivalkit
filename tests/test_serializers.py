import collections
import pickle
import tempfile

import pytest

from revivalkit import serializers


@pytest.fixture
def text_file(request):
    f = tempfile.NamedTemporaryFile(mode='w+')

    def finalizer():
        f.close()

    request.addfinalizer(finalizer)
    return f


def test_json_dump(text_file):
    serializers.json.dump(
        collections.OrderedDict([('name', 'mosky'), ('numbers', [19, 42])]),
        text_file.name,
    )
    text_file.flush()
    assert text_file.read() == '{"name": "mosky", "numbers": [19, 42]}'


@pytest.fixture
def text_file_with_content(request):
    f = text_file(request)
    f.write('{"name": "mosky", "numbers": [19, 42]}')
    f.flush()
    return f


def test_json_load(text_file_with_content):
    assert serializers.json.load(text_file_with_content.name) == {
        'name': 'mosky', 'numbers': [19, 42],
    }


class Thing(object):

    def __init__(self):
        super(Thing, self).__init__()
        self.a = 3

    def say_hello(self):
        print('hello!')


@pytest.fixture
def thing():
    return Thing()


@pytest.fixture
def binary_file(request):
    f = tempfile.NamedTemporaryFile()

    def finalizer():
        f.close()

    request.addfinalizer(finalizer)
    return f


def test_pickle_dump(capsys, binary_file, thing):
    serializers.pickle.dump(thing, binary_file.name)
    binary_file.flush()
    o = pickle.load(binary_file)
    assert o.a == 3

    o.say_hello()
    assert capsys.readouterr() == ('hello!\n', '')


@pytest.fixture
def binary_file_with_content(request):
    f = binary_file(request)
    pickle.dump(thing(), f)
    f.flush()
    return f


def test_pickle_load(capsys, binary_file_with_content):
    o = serializers.pickle.load(binary_file_with_content.name)
    assert o.a == 3

    o.say_hello()
    assert capsys.readouterr() == ('hello!\n', '')
