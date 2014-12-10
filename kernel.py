import sys

import libs
from filesystem import FileSystem
from shell import Shell


class Kernel(object):
    def __init__(self):
        self.filesystem = FileSystem()
        self.virtualize()

    def boot(self):
        self.virtualize()

    def virtualize(self):
        new_modules = dict((name, getattr(libs, name)) for name in libs.__all__)
        sys.modules.update(new_modules)
        self.filesystem.patch_all()

    def run_code(self, code):
        code = compile(code, '<string>', 'exec')
        original_modules = sys.modules.copy()
        new_modules = dict((name, getattr(libs, name)) for name in libs.__all__)
        sys.modules.update(new_modules)
        try:
            exec code in dict()
        finally:
            sys.modules = original_modules


if __name__ == '__main__':
    kernel = Kernel()
    Shell(kernel).run()