pykern
======

Just For Fun. Virtual kernel in python
Still sharing many functions from host, getting separated.

```sh
acuros@AcurosDevMachine ~/Documents/pykern (master)$ python manage.py install -f
acuros@AcurosDevMachine ~/Documents/pykern (master)$ python manage.py run
$ ls
python ls cat
$ ls -l
888 python
568 ls
703 cat
$ python
Pykern Python Interpreter v0.2
>>> import os
>>> os.listdir('.')
[u'python', u'ls', u'cat']
>>> with open('asdf.txt', 'w') as f:
...   f.write('test')
... 
>>> with open('asdf.txt', 'r') as f:
...   print f.read()
... 
test
>>> 
$ 
$ 
$ ls
python ls cat asdf.txt
$ cat asdf.txt
test
$ 
acuros@AcurosDevMachine ~/Documents/pykern (master)$ ls
manage.py  pykern  pykern.fs  tests
acuros@AcurosDevMachine ~/Documents/pykern (master)$ ls -l
total 1040
-rw-rw-r-- 1 acuros acuros     836 Dec 12 11:50 manage.py
drwxrwxr-x 4 acuros acuros    4096 Dec 12 14:45 pykern
-rw-rw-r-- 1 acuros acuros 1050739 Dec 12 18:38 pykern.fs
drwxrwxr-x 4 acuros acuros    4096 Dec 12 13:57 tests

```
