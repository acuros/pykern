import argparse
import math
import os
from pykern.filesystem import FileSystem


parser = argparse.ArgumentParser()
parser.add_argument('-l', action='store_true')
parser.add_argument('-a', action='store_true')
parser.add_argument('directory', nargs='?', default='.')
args = parser.parse_args()


def get_filenames():
    global args
    names = os.listdir(args.directory)
    if args.a:
        names += ['.', '..']
    return sorted(names)


if args.l:
    fs = FileSystem()
    filenames = get_filenames()
    filepaths = [os.path.abspath(os.path.join(args.directory, name)) for name in filenames]
    stats = [(name, os.stat(path)) for name, path in zip(filenames, filepaths)]
    max_size = max([stat.st_size for _, stat in stats])
    if max_size == 0:
        size_buffer = 2
    else:
        size_buffer = str(int(math.log(max_size, 10)) + 1)
    for name, stat in stats:
        mode = 'd' if stat.is_directory() else '-'
        print '%s %{0}d %s'.format(size_buffer) % (mode, stat.st_size, name)
else:
    print ' '.join(get_filenames())
