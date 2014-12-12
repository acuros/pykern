import os
from collections import OrderedDict
from StringIO import StringIO

import bson

from pykern.utils import singleton


class FStringIO(StringIO):
    def __init__(self, filename, data=''):
        self.filename = filename
        StringIO.__init__(self, data)

    def __enter__(self):
        return self

    def __exit__(self, *arg):
        self.close()

    def close(self):
        FileSystem(None).close_file(self)
        StringIO.close(self)


@singleton
class FileSystem(object):
    def __init__(self, fs_file_name):
        self.fs_file_name = fs_file_name
        try:
            self.fs_file = open(self.fs_file_name, 'r+')
        except IOError:
            with open(self.fs_file_name, 'w') as f:
                f.write('\x00'*1024*1024)
                f.seek(0)
                f.write(bson.dumps(dict(metadata=[])))
            self.fs_file = open(self.fs_file_name, 'r+')
        self.metadata = self._load_metadata()
        self.opened_files = dict()

    def _load_metadata(self):
        raw_data = self.fs_file.read(1024*1024)
        metadata = bson.loads(raw_data)['metadata']
        return OrderedDict(metadata)

    def open_file(self, filename, mode='r'):
        if mode.startswith('r'):
            fp = self._open_file_for_read(filename)
        elif mode.startswith('w'):
            fp = self._open_file_for_write(filename)
        else:
            raise AttributeError('Mode have to be set "r" or "w"')
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
            data = vfile.read()
            self.fs_file.write(data)
            self.metadata[vfile.filename]['file_size'] = len(data)
            del self.metadata[vfile.filename]['is_new']
            self.save_metadata()
        self.fs_file.flush()

    def _move_fs_cursor_to(self, filename):
        start_pos = 1024*1024
        for _filename, _metadata in self.metadata.items():
            if _filename == filename:
                break
            start_pos += _metadata['file_size']
        self.fs_file.seek(start_pos)

    def save_metadata(self):
        self.fs_file.seek(0)
        self.fs_file.write(bson.dumps(dict(metadata=self.metadata)))

    @staticmethod
    def empty_metadata():
        return dict(file_size=0)

    def patch_all(self):
        import __builtin__
        __builtin__.open = __builtin__.file = self.open_file

