with open('write.txt', 'w') as f:
    f.write('Hi there.')

with open('write.txt', 'r') as f:
    data = f.read()

assert data == 'Hi there.'