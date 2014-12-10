import sys

import libs
from filesystem import FileSystem
from shell import Shell


class Kernel(object):
    def __init__(self):
        self.filesystem = FileSystem()
        self.subtitue_libs()

    def boot(self):
        Shell(self).run()

    def subtitue_libs(self):
        new_modules = dict((name, getattr(libs, name)) for name in libs.__all__)
        sys.modules.update(new_modules)
        self.filesystem.patch_all()

    def run_file(self, filename):
        with open(filename) as f:
            return self.run_code(f.read())

    def run_code(self, code):
        try:
            exec compile(code, '<string>', 'exec') in dict()
        except:
            return 1
        else:
            return 0


if __name__ == '__main__':
    Kernel().boot()