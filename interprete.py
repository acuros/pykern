import gc
while True:
    execfile(raw_input('filename > '), {})
    gc.collect()
