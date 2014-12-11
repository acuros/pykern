import os

with open('NewFile', 'w') as f:
    f.write('hi')

assert 'NewFile' in  os.listdir('.')