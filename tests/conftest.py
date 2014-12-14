import os
from pykern.emulator import Emulator


def pytest_configure():
    try:
        os.remove('pykern.test.fs')
    except OSError:
        pass
    Emulator.init_disk('pykern.test.fs')


def pytest_unconfigure():
    try:
        os.remove('pykern.test.fs')
    except OSError:
        pass
