import gc


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
            if not command:
                continue
            args = command.split()
            try:
                self.kernel.run_file(args[0], args)
            except IOError:
                print '%s: command not found' % args[0]
            else:
                gc.collect()