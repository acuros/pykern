import os as os_
from pykern.filesystem import FileSystem

[globals().update({name: getattr(os_, name)}) for name in dir(os_)]


def listdir(path):
    return FileSystem(None).metadata.keys()
