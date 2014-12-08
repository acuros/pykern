from filesystem import FileSystem
from shell import Shell
from utils import singleton


@singleton
class Kernel(object):
    def __init__(self):
        self.filesystem = FileSystem()

    @property
    def namespace(self):
        return {'open': self.filesystem.open_file}

    def run_file(self, filename):
        execfile(filename, self.namespace)

if __name__ == '__main__':
    kernel = Kernel()
    Shell(kernel).run()