while True:
    namespaces = {}
    with open(raw_input('filename > ')) as f:
        code = compile(f.read(), '<string>', 'exec')
        exec code in namespaces
