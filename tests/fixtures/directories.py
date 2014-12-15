import os

with open('NewFile', 'w') as f:
    f.write('hi')
assert 'NewFile' in os.listdir('.')
print 'File listdir passed'

os.mkdir('test_dir')
assert 'test_dir' in os.listdir('.')
print 'Directory listdir passed'

assert os.path.isdir('test_dir')
assert not os.path.isdir('NewFile')
print 'isdir passed'

os.rmdir('test_dir')

try:
    os.rmdir('NewFile')
except OSError:
    pass
else:
    raise AssertionError('Can remove not a directory')
