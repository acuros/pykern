from pykern.filesystem import FileSystem
import base as os

__all__ = ['normcase', 'isdir', 'join', 'isabs', 'normpath', 'abspath']

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


def isabs(s):
    """Test whether a path is absolute"""
    return s.startswith('/')


def normpath(path):
    """Normalize path, eliminating double slashes, etc."""
    # Preserve unicode (if path is unicode)
    slash, dot = (u'/', u'.') if isinstance(path, unicode) else ('/', '.')
    if path == '':
        return dot
    initial_slashes = path.startswith('/')
    # POSIX allows one or two initial slashes, but treats three or more
    # as single slash.
    if (initial_slashes and
            path.startswith('//') and not path.startswith('///')):
        initial_slashes = 2
    comps = path.split('/')
    new_comps = []
    for comp in comps:
        if comp in ('', '.'):
            continue
        if (comp != '..' or (not initial_slashes and not new_comps) or
                (new_comps and new_comps[-1] == '..')):
            new_comps.append(comp)
        elif new_comps:
            new_comps.pop()
    comps = new_comps
    path = slash.join(comps)
    if initial_slashes:
        path = slash*initial_slashes + path
    return path or dot


def abspath(path):
    """Return an absolute path."""
    if not isabs(path):
        if isinstance(path, unicode):
            cwd = os.getcwdu()
        else:
            cwd = os.getcwd()
        path = join(cwd, path)
    return normpath(path)
