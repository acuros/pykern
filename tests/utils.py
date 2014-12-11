import os
import traceback

from pykern.emulator import Emulator


def run_file_in_kernel(filename):
    try:
        dirname = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fixtures')
        Emulator().run_external_file(os.path.join(dirname, filename))
    except:
        traceback.print_exc()
        return False
    else:
        return True


