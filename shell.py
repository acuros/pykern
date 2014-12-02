import gc


class Shell(object):
    def __init__(self):
        pass

    @staticmethod
    def run():
        while True:
            execfile(raw_input('Input filename > '), {})
            gc.collect()