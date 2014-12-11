import gc


class Shell(object):
    def __init__(self, kernel):
        self.kernel = kernel

    def run(self):
        while True:
            try:
                filename = raw_input('$ ')
            except EOFError:
                print
                break
            try:
                self.kernel.run_file(filename)
            except IOError:
                print 'File "%s" not found' % filename
            else:
                gc.collect()
