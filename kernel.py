import sys

import libs
from filesystem import FileSystem
from shell import Shell
from utils import singleton


@singleton
class Kernel(object):
    def __init__(self):
        self.filesystem = FileSystem()

    @property
    def namespace(self):
        return {
            'open': self.filesystem.open_file,
            'file': self.filesystem.open_file,
        }

    def run_file(self, filename):
        original_modules = sys.modules.copy()
        new_modules = dict((name, getattr(libs, name)) for name in libs.__all__)
        sys.modules.update(new_modules)
        try:
            execfile(filename, self.namespace)
        finally:
            sys.modules = original_modules

if __name__ == '__main__':
    kernel = Kernel()
    Shell(kernel).run()