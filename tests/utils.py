import os
import traceback

from pykern.emulator import Emulator


def run_file_in_kernel(filename):
    dirname = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fixtures')
    return Emulator().run_external_file(os.path.join(dirname, filename))


