import os
import bson
from filesystem import FileSystem
from kernel import Kernel


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


def test_kernel_file_write():
    dirname = os.path.dirname(os.path.realpath(__file__))
    kernel = Kernel()
    kernel.run_file(os.path.join(dirname, 'file_write_test_in_kernel.py'))