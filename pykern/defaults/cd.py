import os
import sys

if len(sys.argv) < 2:
    path = '/'
else:
    path = sys.argv[1]


os.chdir(path)