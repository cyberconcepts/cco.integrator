'''
Operating system utilities
  
2019-06-19 helmutm@cy55.de
'''

from asyncio import sleep
from os.path import abspath, join
import argparse, os, signal, sys

# command line parsing

def cmdlineArgs(system='???', cfgname='config.yaml'):
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--cfgname", help="config file name (config.yaml)",
                        type=str, default=cfgname)
    args = parser.parse_args()
    if not args:
        exit(-1)
    #print('args: {}'.format(args))
    return vars(args)

# filesystem utilities

def makePath(home, path=None, filename=None, createdirs=False):
    if path is None:
        path = home
    elif not path.startswith('/'):
        path = join(home, path)
    path = abspath(path)
    if createdirs:
        os.makedirs(path)
    return filename and join(path, filename) or path

# process utilities

def savepid(home, path=None, filename='cco.integrator.pid'):
    p = makePath(home, path, filename, createdirs=True)
    with open(p, 'w') as f: 
        f.write(getpid())

def getpid():
    return os.getpid()

async def wait(t=0.1):
    await sleep(t)

def exit(code=0):
    os._exit(code)

def terminate(sig=signal.SIGTERM):
    os.kill(getpid(), sig)
