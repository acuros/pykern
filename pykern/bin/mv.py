import argparse
from os.path import abspath
from pykern.filesystem import FileSystem

parser = argparse.ArgumentParser()
parser.add_argument('source')
parser.add_argument('dest')

args = parser.parse_args()
fs = FileSystem()

src = fs.get_superblock(args.source)

try:
    dest = fs.get_superblock(args.dest)
except OSError:
    pass
fs.superblocks[abspath(args.dest)] = src.copy()
del fs.superblocks[abspath(args.source)]
fs.save_superblocks()
