import sys
from emulator import Emulator

if len(sys.argv) < 2:
    print 'Command required'
    sys.exit(1)

command = sys.argv[1]

emulator = Emulator()

if command == 'install':
    fs_file_name = None
    if len(sys.argv) >= 3:
        fs_file_name = sys.argv[2]
    emulator.install(fs_file_name)
else:
    print 'Command "%s" not found' % command
    sys.exit(1)
