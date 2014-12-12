import glob
import os
import sys

from pykern.filesystem import FileSystem
from kernel import Kernel


class Emulator(object):
    def run_external_file(self, filename, fs_file_name):
        import __builtin__
        names = dir(__builtin__)
        original_builtins = dict((name, getattr(__builtin__, name)) for name in names)
        with open(filename, 'r') as f:
            code = f.read()

        original_modules = sys.modules.copy()
        deep_original_modules = self._copy_original_modules()
        is_success = Kernel(fs_file_name).run_code(code)
        [setattr(__builtin__, name, value) for name, value in original_builtins.items()]
        sys.modules = original_modules
        for module_name, module_copy in deep_original_modules.items():
            for name, value in module_copy.items():
                setattr(sys.modules[module_name], name, value)
        return is_success

    def install(self, fs_file_name, force=False):
        if os.path.exists(fs_file_name):
            if not force:
                raise ValueError('Already installed')
            else:
                os.remove(fs_file_name)
        FileSystem(fs_file_name)
        defaults_dir = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'defaults')
        defaults = glob.glob(os.path.join(defaults_dir, '*.py'))
        for filepath in defaults:
            self.put_file(filepath, fs_file_name)

    def put_file(self, filepath, fs_file_name=None):
        with open(filepath, 'rb') as rf:
            filename = '.'.join(os.path.split(filepath)[1].split('.')[:-1])
            with FileSystem(fs_file_name).open_file(filename, 'w') as vf:
                while True:
                    data = rf.read(10240)
                    if not data:
                        break
                    vf.write(data)

    def _copy_original_modules(self):
        import libs
        original_module_names = [name.split('pykern_')[1] for name in libs.__all__]
        original_modules = dict()
        for module_name in original_module_names:
            original_modules[module_name] = dict(
                (name, getattr(sys.modules[module_name], name))
                for name in dir(sys.modules[module_name])
            )
        return original_modules