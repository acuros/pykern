import bson
import glob
import os
import stat
import sys

from pykern.filesystem import FileSystem
from kernel import Kernel
from pykern.libs import patch_libs


class Emulator(object):
    def boot(self, disk_file_name='pykern.fs'):
        with open(disk_file_name, 'r+') as disk:
            self.ready_kernel(disk).boot()

    def run_external_file(self, filename, disk_file_name):
        import __builtin__
        names = dir(__builtin__)
        original_builtins = dict((name, getattr(__builtin__, name)) for name in names)
        with open(filename, 'r') as f:
            code = f.read()

        original_modules = sys.modules.copy()
        deep_original_modules = self._copy_original_modules()
        with open(disk_file_name, 'r+') as disk:
            kernel = self.ready_kernel(disk)
            is_success = kernel.run_code(code)

        [setattr(__builtin__, name, value) for name, value in original_builtins.items()]
        sys.modules = original_modules
        for module_name, module_copy in deep_original_modules.items():
            for name, value in module_copy.items():
                setattr(sys.modules[module_name], name, value)
        return is_success

    def install(self, disk_file_name, force=False):
        if os.path.exists(disk_file_name):
            if not force:
                raise ValueError('Already installed')

        with open(disk_file_name, 'wb+') as disk:
            disk.write('\x00'*1024*1024)
            disk.seek(0, 0)
            disk.write(bson.dumps(dict(metadata=[])))
            disk.seek(0, 0)

            fs = FileSystem(disk)

            fs.add_item('/', fs.DIRECTORY_MODE)

            bin_dir = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'bin')
            bins = glob.glob(os.path.join(bin_dir, '*.py'))
            fs.add_item('/bin', fs.DIRECTORY_MODE)

            for filepath in bins:
                self.put_file(filepath, '/bin', disk_file_name)

    def ready_kernel(self, disk):
        kernel = Kernel(disk)
        kernel.filesystem.patch_all()
        patch_libs()
        return kernel

    @staticmethod
    def init_disk(disk_file_name):
        with open(disk_file_name, 'w') as disk:
            disk.write('\x00'*1024*1024)
            disk.seek(0)
            disk.write(bson.dumps(dict(metadata=[('/', dict(size=0, mode=stat.S_IFDIR))])))

    def put_file(self, src, dst='/', fs_file_name=None):
        with open(src, 'rb') as rf:
            filename = '.'.join(os.path.split(src)[1].split('.')[:-1])
            filename = os.path.join(dst, filename)
            with open(fs_file_name, 'r+') as disk:
                with FileSystem(disk).open_file(filename, 'w') as vf:
                    self._copy(rf, vf)

    def _copy(self, src, dst, buffer_size=10240):
        data = src.read(buffer_size)
        while data:
            dst.write(data)
            data = src.read(buffer_size)

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