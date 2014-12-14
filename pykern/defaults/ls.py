import argparse
import math
import os


parser = argparse.ArgumentParser()
parser.add_argument('-l', action='store_true')
parser.add_argument('-a', action='store_true')
args = parser.parse_args()


def get_filenames():
    global args
    names = os.listdir('.')
    if args.a:
        names += ['.', '..']
    return sorted(names)


if args.l:
    filenames = get_filenames()
    stats = [(name, os.stat(name)) for name in filenames]
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
