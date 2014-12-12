import argparse
import math
import os

parser = argparse.ArgumentParser()
parser.add_argument('-l', action='store_true')
args = parser.parse_args()

if args.l:
    filenames = os.listdir('.')
    stats = [os.stat(name) for name in filenames]
    stats = dict((name, os.stat(name)) for name in filenames)
    max_size = max([stat.st_size for stat in stats.values()])
    size_buffer = str(int(math.log(max_size, 10)) + 1)
    for name, stat in stats.items():
        print '%{0}d %s'.format(size_buffer) % (stat.st_size, name)
else:
    print ' '.join(os.listdir('.'))
