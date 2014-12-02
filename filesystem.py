from collections import OrderedDict
from StringIO import StringIO
from utils import singleton


class FStringIO(StringIO):
    def __init__(self, filename, data=''):
        self.filename = filename
        StringIO.__init__(self, data)

    def close(self):
        FileSystem().close_file(self)
        StringIO.close(self)


@singleton
class FileSystem(object):
    def __init__(self, fs_file_name='pykern.fs'):
        try:
            self.fs_file = open(fs_file_name, 'r+')
        except IOError:
            open(fs_file_name, 'w').close()
            self.fs_file = open(fs_file_name, 'r+')
        self.metadata = self._load_metadata()
        self.opened_files = dict()

    def _load_metadata(self):
        line = self.fs_file.readline().strip()
        return OrderedDict(line)

    def open_file(self, filename, mode='r'):
        if mode == 'r':
            fp = self._open_file_for_read(filename)
        elif mode == 'w':
            fp = self._open_file_for_write(filename)
        self.opened_files[filename] = mode
        return fp

    def _open_file_for_read(self, filename):
        if filename not in self.metadata:
            raise IOError('File %s is not exists' % filename)
        return FStringIO(filename, self.read_file(filename))

    def _open_file_for_write(self, filename):
        if filename not in self.metadata:
            self.metadata[filename] = self.empty_metadata()
            self.metadata[filename]['is_new'] = True
            return FStringIO(filename)
        else:
            raise NotImplementedError

    def read_file(self, filename):
        self._move_fs_cursor_to(filename)
        return self.fs_file.read(self.metadata[filename]['file_size'])

    def close_file(self, vfile):
        mode = self.opened_files.pop(vfile.filename)
        if mode == 'r':
            return
        if mode == 'w' and 'is_new' in self.metadata[vfile.filename]:
            self.fs_file.seek(0, 2)
            vfile.seek(0)
            self.fs_file.write(vfile.read())
            self.fs_file.flush()
            return
        gap = vfile.len - self.metadata[vfile.filename]['file_size']
        print gap
        if gap == 0:
            return
        metadata = self.metadata.items()
        if gap < 0:
            metadata.reverse()
        for filename, metadata in metadata:
            data = self.read_file(filename)
            self._move_fs_cursor_to(filename)
            self.fs_file.seek(gap, 1)
            self.fs_file.write(data)
            if filename == vfile.filename:
                break
        self.fs_file.flush()

    def _move_fs_cursor_to(self, filename):
        start_pos = 0
        for _filename, _metadata in self.metadata.items():
            if _filename == filename:
                break
            start_pos += _metadata['file_size']
        self.fs_file.seek(start_pos)

    def empty_metadata(self):
        return dict(file_size=0)
