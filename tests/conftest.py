from _pytest.monkeypatch import monkeypatch

import os


def pytest_configure():
    try:
        os.remove('pykern.test.fs')
    except OSError:
        pass
    patch = monkeypatch()
    patch.setenv('PYKERN_FS_FILENAME', 'pykern.test.fs')


def pytest_unconfigure():
    try:
        os.remove('pykern.test.fs')
    except OSError:
        pass
