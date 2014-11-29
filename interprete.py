from sys import argv as __argv
with open(__argv[1]) as __f:
    exec(__f.read())