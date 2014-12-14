import stat
import bson

from collections import OrderedDict
from StringIO import StringIO


class FStringIO(StringIO):
    def __init__(self, filename, data=''):
        self.filename = filename
        StringIO.__init__(self, data)

    def __enter__(self):
        return self

    def __exit__(self, *arg):
        self.close()

    def close(self):
        FileSystem().close_file(self)
        StringIO.close(self)


class FileSystemSingleton(type):
    _disks = {}

    def __call__(cls, fd=None):
        if fd is None:
            if not cls._disks:
                raise TypeError('No disk loaded. Disk fd is required')
            if len(cls._disks) > 1:
                raise TypeError('More than one disk loaded. Disk fd is required')
            disk = cls._disks.values()[0]
            if disk['fd'].closed:
                raise TypeError('Loaded disk fd is already closed. Disk fd is required')
            return disk['instance']

        disk = cls._disks.get(fd.name)
        if not disk or disk['fd'].closed:
            instance = super(FileSystemSingleton, cls).__call__(fd)
            cls._disks[fd.name] = dict(instance=instance, fd=fd)
        else:
            instance = disk['instance']
        return instance


class FileSystem(object):
    __metaclass__ = FileSystemSingleton

    FILE_MODE = stat.S_IFREG
    DIRECTORY_MODE = stat.S_IFDIR

    def __init__(self, disk=None):
        if disk is None:
            raise TypeError('Disk fd is omitted')
        self.disk = disk
        self.metadata = self._load_metadata()
        self.current_dir = '/'
        self.opened_files = dict()
        self.commands = FileSystemCommands(self)

    def _load_metadata(self):
        raw_data = self.disk.read(1024*1024)
        return OrderedDict(bson.loads(raw_data)['metadata'])

    def open_file(self, filename, mode='r'):
        filename = self.get_absolute_of(filename)
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
            self.add_item(filename, stat.S_IFREG, True)
            return FStringIO(filename)
        else:
            raise NotImplementedError

    def read_file(self, filename):
        self._move_fs_cursor_to(filename)
        return self.disk.read(self.metadata[filename]['size'])

    def close_file(self, vfile):
        mode = self.opened_files.pop(vfile.filename)
        if mode == 'r':
            return
        if mode == 'w' and 'is_new' in self.metadata[vfile.filename]:
            self.disk.seek(0, 2)
            vfile.seek(0)
            data = vfile.read()
            self.disk.write(data)
            self.metadata[vfile.filename]['size'] = len(data)
            del self.metadata[vfile.filename]['is_new']
            self.save_metadata()
        self.disk.flush()

    def add_item(self, name, mode=0, is_new=False, size=0):
        absolute_name = self.get_absolute_of(name)
        self.metadata[absolute_name] = dict(size=size, mode=mode)
        if is_new:
            self.metadata[absolute_name]['is_new'] = True

    def get_absolute_of(self, path):
        return _calculate_absolute(self.current_dir, path)

    def _move_fs_cursor_to(self, filename):
        start_pos = 1024*1024
        for _filename, _metadata in self.metadata.items():
            if _filename == filename:
                break
            start_pos += _metadata['size']
        self.disk.seek(start_pos)

    def save_metadata(self):
        self.disk.seek(0)
        self.disk.write(bson.dumps(dict(metadata=self.metadata.items())))

    @staticmethod
    def empty_metadata():
        return dict(mode=0, size=0)

    def patch_all(self):
        import __builtin__
        __builtin__.open = __builtin__.file = self.open_file


class FileSystemCommands(object):
    def __init__(self, filesystem):
        self.filesystem = filesystem


def is_relative_path(path):
    return not path.startswith('/')


def _calculate_absolute(current_dir, path):
    if not is_relative_path(path):
        return path

    current_dentries = [dentry for dentry in current_dir.split('/') if dentry]
    dentries_to_apply = path.split('/')
    while dentries_to_apply:
        next_dentry = dentries_to_apply.pop(0)
        if next_dentry in ('', '.'):
            continue
        elif next_dentry == '..':
            if len(current_dentries) > 0:
                current_dentries.pop()
        else:
            current_dentries.append(next_dentry)
    return '/%s' % '/'.join(current_dentries)
