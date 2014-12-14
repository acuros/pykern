import readline
import gc
import os


class Shell(object):
    def __init__(self, kernel):
        self.kernel = kernel

    def run(self):
        while True:
            try:
                command = raw_input('$ ').strip()
            except EOFError:
                print
                break
            except KeyboardInterrupt:
                print
                continue
            if not command:
                continue
            args = command.split()
            try:
                self.kernel.run_file(os.path.join('/bin', args[0]), args)
            except IOError:
                print '%s: command not found' % args[0]
            else:
                gc.collect()