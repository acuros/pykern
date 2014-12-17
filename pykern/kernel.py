import sys

from filesystem import FileSystem


class Kernel(object):
    def __init__(self, disk):
        self.filesystem = FileSystem(disk)

    def boot(self):
        from pykern.shell import Shell
        Shell(self).run()

    def run_file(self, filename, args):
        with open(filename) as f:
            sys.argv = args
            result = self.run_code(f.read())
            sys.argv = []
            return result

    def run_code(self, code):
        try:
            exec compile(code, '<string>', 'exec') in {'__name__': '__main__'}
        except Exception, e:
            print e
            return False
        else:
            return True
