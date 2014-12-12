from pykern.filesystem import FileSystem


class stat_result(object):
    def __init__(self, st_mode, st_size):
        self.st_mode = st_mode
        self.st_size = st_size

    def __repr__(self):
        return '<stat_result: st_size=%d>' % self.st_size


def mkdir(dirname):
    FileSystem().mkdir(dirname)


def listdir(path):
    return FileSystem().metadata.keys()


def stat(path):
    try:
        file_ = FileSystem().metadata[path]
    except KeyError:
        raise OSError('No such file "%s"' % path)

    return stat_result(file_['mode'], file_['size'])
