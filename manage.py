import argparse
import sys

from pykern.emulator import Emulator
from pykern.kernel import Kernel

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

install_parser = subparsers.add_parser('install')
install_parser.set_defaults(command='install')
install_parser.add_argument('fs_file_name', nargs='?', default='pykern.fs')
install_parser.add_argument('-f', '--force', action='store_true')

run_parser = subparsers.add_parser('run')
run_parser.set_defaults(command='run')
run_parser.add_argument('fs_file_name', nargs='?', default='pykern.fs')

args = parser.parse_args()

emulator = Emulator()

if args.command == 'install':
    emulator.install(args.fs_file_name, args.force)
elif args.command == 'run':
    emulator.boot(args.fs_file_name)
else:
    print 'Command "%s" not found' % args.command
    sys.exit(1)
