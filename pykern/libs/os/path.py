from pykern.filesystem import FileSystem

__all__ = ['normcase', 'isdir', 'join']

normcase = lambda p: p


def isdir(path):
    try:
        FileSystem().get_superblock(path, mode=FileSystem.DIRECTORY_MODE)
    except OSError:
        return False
    else:
        return True


def join(a, *p):
    """Join two or more pathname components, inserting '/' as needed.
    If any component is an absolute path, all previous path components
    will be discarded."""
    path = a
    for b in p:
        if b.startswith('/'):
            path = b
        elif path == '' or path.endswith('/'):
            path += b
        else:
            path += '/' + b
    return path
