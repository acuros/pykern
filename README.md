pykern
======

Just For Fun. Virtual kernel in python
Still sharing many functions from host, getting separated.

```sh
acuros@AcurosDevMachine ~/Documents/pykern (master)$ python manage.py install -f
acuros@AcurosDevMachine ~/Documents/pykern (master)$ python manage.py run
/ $ ls -al
d  0 .
d  0 ..
d  0 bin
/ $ cd bin
/bin $ ls -al
d   0 .
d   0 ..
- 721 cat
- 104 cd
- 805 ls
- 148 mkdir
-  28 pwd
- 888 python
/bin $ cat pwd
import os

print os.getcwd()
/bin $ python
Pykern Python Interpreter v0.2
>>> with open('/foo', 'w') as f:
...   f.write('test')
... 
>>> with open('/foo', 'r') as f:
...   print f.read()
... 
test
>>> 
/bin $ cd ..
/ $ ls -al
d 0 .
d 0 ..
d 0 bin
- 4 foo
/ $ cat foo
test
/ $
acuros@AcurosDevMachine ~/Documents/pykern (master)$ ls
manage.py  pykern  pykern.fs  tests
acuros@AcurosDevMachine ~/Documents/pykern (master)$ ls -l
total 1040
-rw-rw-r-- 1 acuros acuros     836 Dec 12 11:50 manage.py
drwxrwxr-x 4 acuros acuros    4096 Dec 12 14:45 pykern
-rw-rw-r-- 1 acuros acuros 1050739 Dec 12 18:38 pykern.fs
drwxrwxr-x 4 acuros acuros    4096 Dec 12 13:57 tests

```
