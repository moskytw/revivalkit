import pickle
import tempfile

import pytest

from revivalkit import serializers


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


def test_highest_pickle_dump(capsys, binary_file, thing):
    serializers.highest_pickle.dump(thing, binary_file)
    binary_file.flush()
    binary_file.seek(0)

    o = pickle.load(binary_file)
    assert o.a == 3
    o.say_hello()
    assert capsys.readouterr() == ('hello!\n', '')


@pytest.fixture
def file_with_pickle(request):
    f = binary_file(request)
    pickle.dump(thing(), f)
    f.flush()
    f.seek(0)
    return f


def test_highest_pickle_load(capsys, file_with_pickle):
    o = serializers.highest_pickle.load(file_with_pickle)
    assert o.a == 3
    o.say_hello()
    assert capsys.readouterr() == ('hello!\n', '')
