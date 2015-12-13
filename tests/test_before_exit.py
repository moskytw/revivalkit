import os
import signal
import sys

import pytest

from revivalkit import before_exit


pid = os.getpid()


@pytest.fixture
def backup_sigint_handler(request):
    handler = signal.getsignal(signal.SIGINT)

    def finalizer():
        signal.signal(signal.SIGINT, handler)

    request.addfinalizer(finalizer)
    return handler


def test_mute_default_sigint(capsys, backup_sigint_handler):
    before_exit._mute_sigint()
    os.kill(pid, signal.SIGINT)
    assert capsys.readouterr() == (
        '', '{}: still cleaning up ...\n'.format(sys.argv[0]),
    )


def custom_sigint_handler(signum, frame):
    pass


@pytest.fixture
def change_sigint_handler(backup_sigint_handler):
    signal.signal(signal.SIGINT, custom_sigint_handler)
    os.kill(pid, signal.SIGINT)     # Make sure the handler is changed.
    return custom_sigint_handler


def test_restore_sigint(capsys, change_sigint_handler):
    before_exit._restore_sigint()
    with pytest.raises(KeyboardInterrupt):
        os.kill(pid, signal.SIGINT)


def test_mute_restore_custom_sigint(change_sigint_handler):
    assert signal.getsignal(signal.SIGINT) is custom_sigint_handler

    before_exit._mute_sigint()
    assert (
        signal.getsignal(signal.SIGINT)
        is before_exit._print_still_working_message
    )

    before_exit._restore_sigint()
    assert signal.getsignal(signal.SIGINT) is custom_sigint_handler
