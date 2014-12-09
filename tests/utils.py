import os
import traceback

from kernel import Kernel


def run_file_in_kernel(filename):
    try:
        dirname = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fixtures')
        kernel = Kernel()
        kernel.run_file(os.path.join(dirname, filename))
    except:
        traceback.print_exc()
        return False
    else:
        return True


