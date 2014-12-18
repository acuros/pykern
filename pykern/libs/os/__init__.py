from . import base, path

__all__ = ['path']
__all__.extend(list(base.__all__))
from base import *

import sys
sys.modules['os.path'] = path
