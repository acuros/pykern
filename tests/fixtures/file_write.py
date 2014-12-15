with open('write.txt', 'w') as f:
    f.write('Hi there.')

with open('write.txt', 'r') as f:
    data = f.read()

assert data == 'Hi there.'

f = file('write2.txt', 'w')
f.write('Hello')
f.close()

with open('write2.txt', 'r') as f:
    data = f.read()

assert data == 'Hello'


import os
os.remove('write.txt')
os.remove('/write2.txt')
try:
    os.remove('non-exists')
except OSError:
    pass
else:
    raise AssertionError('Can remove not exists file')
