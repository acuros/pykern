from filesystem import FileSystem
import os


def test_file_write():
    fs = FileSystem('test.file.txt')
    f = fs.open_file('file.txt', 'w')
    f.write('1234')
    f.close()
    assert os.path.getsize('test.file.txt') > 0