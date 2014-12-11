from os import *
from pykern.filesystem import FileSystem


def listdir(path):
    return FileSystem().metadata.keys()
