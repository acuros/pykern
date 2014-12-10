import sys
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
