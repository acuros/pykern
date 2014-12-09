import bson

from filesystem import FileSystem
from tests.utils import run_file_in_kernel


def test_filesystem_file_write():
    fs = FileSystem()
    with fs.open_file('file.txt', 'w') as f:
        f.write('1234')

    with open(fs.fs_file_name, 'r') as f:
        data = f.read()
    assert len(data) > 0

    assert data[1024*1024:] == '1234'

    metadata = bson.loads(data)['metadata']
    assert metadata['file.txt']['file_size'] == 4


def test_filesystem_in_kernel():
    assert run_file_in_kernel('file_write.py')
