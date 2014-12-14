import argparse
import readline


def read_mode(filenames):
    for filename in filenames:
        try:
            with open(filename, 'r') as f:
                print f.read()
        except IOError:
            print 'cat: %s: No such file or directory' % filename


def copy_mode():
    readline.parse_and_bind('C-d: accept-line')
    while True:
        try:
            line = raw_input('')
        except KeyboardInterrupt:
            break
        except EOFError:
            line = None
        if not line:
            break
        print line


parser = argparse.ArgumentParser()
parser.add_argument('file', nargs='*')
args = parser.parse_args()

if args.file:
    read_mode(args.file)
else:
    copy_mode()
