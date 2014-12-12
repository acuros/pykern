import sys
from importlib import import_module

from . import pykern_os

__all__ = ['pykern_os']


def patch_libs():
    for module_name in __all__:
        original_name = module_name.split('pykern_')[1]
        new_module = globals()[module_name]
        original_module = import_module(original_name)

        names_in_original_module = dir(original_module)
        names_to_be_changed = [name for name in dir(new_module) if name in names_in_original_module]
        for name in names_to_be_changed:
            setattr(original_module, name, getattr(new_module, name))

        for name in names_in_original_module:
            setattr(new_module, name, getattr(original_module, name))

        sys.modules.update(dict(original_name=new_module))