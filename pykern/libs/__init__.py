import sys
from . import os

__all__ = ['os']


def patch_libs():
    for module_name in __all__:
        new_module = globals()[module_name]
        sys.modules.update({module_name: new_module})
