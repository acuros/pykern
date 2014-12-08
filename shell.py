import gc


class Shell(object):
    def __init__(self, kernel):
        self.kernel = kernel

    def run(self):
        while True:
            self.kernel.run_file(raw_input('Input filename > '))
            gc.collect()
