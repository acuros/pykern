from pykern.filesystem import FileSystem

import os


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
    if dirname in fs.metadata or dirname in ('.', '..'):
        raise IOError('File exists')
    if '/' in dirname:
        raise ValueError('"/" is not permitted in directory name')
    fs.add_item(dirname, stat.S_IFDIR)


def getcwd():
    return FileSystem().current_dir


def chdir(path):
    fs = FileSystem()
    absolute_path = fs.get_absolute_of('%s' % path)
    if not os.path.isdir(absolute_path):
        raise OSError('Not a directory: "%s"' % path)
    fs.current_dir = absolute_path


def listdir(path):
    fs = FileSystem()
    if not os.path.isdir(path):
        raise OSError('Not a directory: "%s"' % path)
    absolute_target_path = fs.get_absolute_of('%s' % path)
    if not absolute_target_path.endswith('/'):
        absolute_target_path += '/'
    result = [
        path[len(absolute_target_path):]
        for path in FileSystem().metadata
        if path.startswith(absolute_target_path) and
        '/' not in path.split(absolute_target_path, 1)[1] and
        path != absolute_target_path
    ]
    return result


def stat(path):
    fs = FileSystem()
    path = fs.get_absolute_of(path)
    try:
        file_ = fs.metadata[path]
    except KeyError:
        raise OSError('No such file "%s"' % path)

    return stat_result(file_['mode'], file_['size'])