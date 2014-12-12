import os


def pytest_configure():
    try:
        os.remove('pykern.test.fs')
    except OSError:
        pass


def pytest_unconfigure():
    try:
        os.remove('pykern.test.fs')
    except OSError:
        pass
