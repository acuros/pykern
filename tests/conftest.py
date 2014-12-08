import os


def pytest_configure():
    try:
        os.remove('test.file.txt')
    except OSError:
        pass


def pytest_unconfigure():
    try:
        os.remove('test.file.txt')
    except OSError:
        pass
