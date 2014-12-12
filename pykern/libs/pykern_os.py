from pykern.filesystem import FileSystem


class stat_result(object):
    def __init__(self, st_size):
        self.st_size = st_size

    def __repr__(self):
        return '<stat_result: st_size=%d>' % self.st_size


def listdir(path):
    return FileSystem().metadata.keys()


def stat(path):
    return stat_result(0)
