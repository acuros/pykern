import glob
import os
import sys

from pykern.filesystem import FileSystem
from kernel import Kernel


class Emulator(object):
    def run_external_file(self, filename):
        import __builtin__
        names = dir(__builtin__)
        original_builtins = dict((name, getattr(__builtin__, name)) for name in names)
        with open(filename, 'r') as f:
            code = f.read()
        original_modules = sys.modules.copy()
        Kernel().run_code(code)
        [setattr(__builtin__, name, value) for name, value in original_builtins.items()]
        sys.modules = original_modules

    def install(self, fs_file_name=None):
        fs = FileSystem(fs_file_name)
        if not fs.is_created:
            raise ValueError('Already installed')
        defaults_dir = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'defaults')
        defaults = glob.glob(os.path.join(defaults_dir, '*.py'))
        for filepath in defaults:
            self.put_file(filepath, fs_file_name)

    def put_file(self, filepath, fs_file_name=None):
        with open(filepath, 'rb') as rf:
            filename = os.path.split(filepath)[1]
            with FileSystem(fs_file_name).open_file(filename, 'w') as vf:
                while True:
                    data = rf.read(10240)
                    if not data:
                        break
                    vf.write(data)
