'''
Operating system utilities
  
2019-06-19 helmutm@cy55.de
'''

from os.path import abspath, join
import os, signal, sys, time

# filesystem utilities

def makePath(ctx, path=None, filename=None):
    if path is None:
        path = ctx.home
    elif not path.startswith('/'):
        path = join(ctx.home, path)
    path = abspath(path)
    os.makedirs(path)
    return filename and join(path, filename) or path

# process utilities

def savepid(ctx, path=None, filename='cco.integrator.pid'):
    p = makePath(ctx, path, filename)
    f = open(p, 'w')
    f.write(getpid())
    f.close()

def getpid():
    return os.getpid()

def wait(t=0.1):
    time.sleep(t)

def exit(code=0):
    os._exit(code)

def terminate(sig=signal.SIGTERM):
    os.kill(getpid(), sig)
