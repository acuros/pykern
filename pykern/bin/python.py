import readline
import traceback


def line_finished(line):
    return not line.endswith(':')


def main():
    print 'Pykern Python Interpreter v0.2'

    lines = []
    while True:
        indicator_str = '>>> ' if not lines else '... '
        try:
            line = raw_input(indicator_str)
        except EOFError:
            print
            break
        except KeyboardInterrupt:
            lines = []
            print
            continue

        lines.append(line)
        if len(lines) == 1 and line_finished(line) or line == '':
            code = '\n'.join(lines)
            try:
                try:
                    print eval(code)
                except SyntaxError:
                    exec compile(code, '<string>', 'exec')
            except Exception, e:
                traceback.print_exc()

            lines = []


if __name__ == '__main__':
    main()
