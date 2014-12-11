import readline
import traceback

print 'Pykern Python Interpreter v0.1'
lines = []
while True:
    indicator_str = '>>> ' if not lines else '...'
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
    if len(lines) == 1 and not lines[-1].endswith(':') or lines[-1] == '':
        code = '\n'.join(lines)
        try:
            exec compile(code, '<string>', 'exec')
        except Exception, e:
            traceback.print_exc()

        lines = []
