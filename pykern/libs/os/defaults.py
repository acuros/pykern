from pykern.filesystem import FileSystem

__all__ = ['stat_result', 'mkdir', 'getcwd', 'chdir', 'listdir', 'remove', 'rmdir', 'stat']

from . import path


class stat_result(object):
    def __init__(self, st_mode, st_size):
        self.st_mode = st_mode
        self.st_size = st_size

    def __repr__(self):
        return '<stat_result: st_mode=%d, st_size=%d>' % (
            self.st_mode, self.st_size,
        )

    def is_directory(self):
        import stat
        return stat.S_ISDIR(self.st_mode)


def mkdir(dirname):
    import stat
    fs = FileSystem()
    if dirname in fs.superblocks or dirname in ('.', '..'):
        raise IOError('File exists')
    if '/' in dirname:
        raise ValueError('"/" is not permitted in directory name')
    fs.add_superblock(dirname, stat.S_IFDIR)


def getcwd():
    return FileSystem().current_directory


def chdir(p):
    fs = FileSystem()
    absolute_path = path.abspath('%s' % p)
    fs.get_superblock(absolute_path, mode=fs.DIRECTORY_MODE)
    fs.current_directory = absolute_path


def listdir(p):
    if not path.isdir(p):
        raise OSError('Not a directory: "%s"' % p)
    absolute_target_path = path.abspath('%s' % p)
    if not absolute_target_path.endswith('/'):
        absolute_target_path += '/'
    result = [
        p[len(absolute_target_path):]
        for p in FileSystem().superblocks
        if p.startswith(absolute_target_path) and
        '/' not in p.split(absolute_target_path, 1)[1] and
        p != absolute_target_path
    ]
    return result


def remove(p):
    FileSystem().remove_file(p)


def rmdir(p):
    FileSystem().remove_directory(p)


def stat(p):
    fs = FileSystem()
    p = path.abspath(p)
    superblock = fs.get_superblock(p)
    return stat_result(superblock['mode'], superblock['size'])
