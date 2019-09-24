'''
Operating system utilities
  
2019-06-19 helmutm@cy55.de
'''

from asyncio import sleep
from os.path import abspath, join
import argparse, os, signal, sys

from cco.integrator import context, dispatcher, registry

# system startup

async def start(home, **params):
    reg = registry.load()
    ctx = context.setup(home=home, registry=reg, **params)
    await dispatcher.start(ctx)
    await wait()
    exit()

# command line parsing

def cmdlineArgs(system='???', cfgname='config.yaml'):
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--cfgname", help="config file name (config.yaml)",
                        type=str, default=cfgname)
    parser.add_argument("-s", "--system", help="operating system (e.g. linux)",
                        type=str, default=system)
    args = parser.parse_args()
    if not args:
        exit(-1)
    #print('args: {}'.format(args))
    return vars(args)

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

async def wait(t=0.1):
    await sleep(t)

def exit(code=0):
    os._exit(code)

def terminate(sig=signal.SIGTERM):
    os.kill(getpid(), sig)
