import bson
from filesystem import FileSystem


def test_file_write():
    fs = FileSystem('test.file.txt')
    with fs.open_file('file.txt', 'w') as f:
        f.write('1234')

    with open('test.file.txt', 'r') as f:
        data = f.read()
    assert len(data) > 0

    assert data[1024*1024:] == '1234'

    metadata = bson.loads(data)['metadata']
    assert metadata['file.txt']['file_size'] == 4