from . import defaults, path

__all__ = ['path']
__all__.extend(list(defaults.__all__))
from defaults import *

import sys
sys.modules['os.path'] = path
