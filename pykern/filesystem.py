import stat
import bson

from collections import OrderedDict
from StringIO import StringIO


class FStringIO(StringIO):
    def __init__(self, filename, data=''):
        self.name = filename
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
        self.superblocks = self._load_superblocks()
        self.current_directory = '/'
        self.opened_files = dict()
        global abspath
        from os.path import abspath

    def _load_superblocks(self):
        raw_data = self.disk.read(1024*1024)
        return OrderedDict(bson.loads(raw_data)['superblocks'])

    def open_file(self, filename, mode='r'):
        filename = abspath(filename)
        if mode.startswith('r'):
            fp = self._open_file_for_read(filename)
        elif mode.startswith('w'):
            fp = self._open_file_for_write(filename)
        else:
            raise AttributeError('Mode have to be set "r" or "w"')
        self.opened_files[filename] = mode
        return fp

    def _open_file_for_read(self, filename):
        if filename not in self.superblocks:
            raise IOError('File %s is not exists' % filename)
        return FStringIO(filename, self.read_file(filename))

    def _open_file_for_write(self, filename):
        if filename not in self.superblocks:
            self.add_superblock(filename, stat.S_IFREG)
            return FStringIO(filename)
        else:
            raise NotImplementedError

    def read_file(self, filename):
        dentry = self.get_superblock(filename, mode=self.FILE_MODE)
        self.disk.seek(1024*1024 + dentry['offset'])
        return self.disk.read(self.superblocks[filename]['size'])

    def close_file(self, vfile):
        mode = self.opened_files.pop(vfile.name)
        if mode == 'r':
            return
        elif mode == 'w':
            self.disk.seek(0, 2)
            vfile.seek(0)
            data = vfile.read()
            self.disk.write(data)
            self.superblocks[vfile.name]['size'] = len(data)
            self.save_superblocks()
        self.disk.flush()

    def remove_file(self, filename):
        self._remove_dentry(filename, self.FILE_MODE)

    def remove_directory(self, filename):
        self._remove_dentry(filename, self.DIRECTORY_MODE)

    def _remove_dentry(self, filename, mode):
        dentry_name = abspath(filename)
        self.get_superblock(dentry_name, mode=mode)
        self.superblocks.pop(dentry_name)

    def get_superblock(self, name, mode=None):
        dentry = self.superblocks.get(abspath(name))
        if dentry and (mode is None or dentry['mode'] == mode):
            return dentry
        elif dentry and mode == self.DIRECTORY_MODE:
            raise OSError("Not a directory: '%s'" % name)
        elif dentry and mode == self.FILE_MODE:
            raise OSError("Is a directory: '%s'" % name)
        elif not dentry:
            raise OSError("No such file or directory: '%s'" % name)

    def add_superblock(self, name, mode=0, size=0):
        absolute_name = abspath(name)
        if self.superblocks.keys():
            last_superblock = self.superblocks[self.superblocks.keys()[-1]]
            offset = last_superblock['offset'] + last_superblock['size']
        else:
            offset = 0
        self.superblocks[absolute_name] = dict(
            size=size, mode=mode, offset=offset
        )

    def save_superblocks(self):
        self.disk.seek(0)
        self.disk.write(bson.dumps(dict(superblocks=self.superblocks.items())))

    def patch_all(self):
        import __builtin__
        __builtin__.open = __builtin__.file = self.open_file
