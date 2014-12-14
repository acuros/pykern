from collections import OrderedDict
import bson

from pykern.filesystem import FileSystem, _calculate_absolute
from tests.utils import run_file_in_kernel


def test_filesystem_file_write():
    with open('pykern.test.fs', 'r+') as disk:
        fs = FileSystem(disk)
        with fs.open_file('file.txt', 'w') as f:
            f.write('1234')

    with open('pykern.test.fs', 'r') as f:
        data = f.read()
    assert len(data) > 0

    assert data[1024*1024:] == '1234'

    superblocks = OrderedDict(bson.loads(data)['superblocks'])
    assert superblocks['/file.txt']['size'] == 4


def test_file_write():
    assert run_file_in_kernel('file_write.py')


def test_directories():
    assert run_file_in_kernel('directories.py')


def test_relative_path():
    assert _calculate_absolute('/', '.') == '/'
    assert _calculate_absolute('/', 'foo') == '/foo'
    assert _calculate_absolute('/', 'foo/bar') == '/foo/bar'
    assert _calculate_absolute('/foo/bar', '..') == '/foo'
    assert _calculate_absolute('/foo/bar/', '../foo') == '/foo/foo'
    assert _calculate_absolute('/', '../../../') == '/'
