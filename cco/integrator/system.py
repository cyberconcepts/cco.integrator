'''
Operating system utilities
  
2019-06-19 helmutm@cy55.de
'''

from asyncio import sleep
from os.path import abspath, join
import argparse, os, signal, sys

from typing import Dict, Optional

# command line parsing

def cmdlineArgs(system: str = '???', 
                cfgname: str ='config.yaml') -> Dict[str, str]:
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--cfgname", help="config file name (config.yaml)",
                        type=str, default=cfgname)
    args = parser.parse_args()
    if not args:
        exit(-1)
    #print('args: {}'.format(args))
    return vars(args)

# filesystem utilities

def makePath(home: str, 
             path: Optional[str] = None, 
             filename: Optional[str] = None, 
             createdirs: bool = False) -> str:
    if path is None:
        path = home
    elif not path.startswith('/'):
        path = join(home, path)
    path = abspath(path)
    if createdirs:
        os.makedirs(path)
    return filename and join(path, filename) or path

# process utilities

def savepid(home: str, 
            path: Optional[str] = None, 
            filename: Optional[str] = 'cco.integrator.pid') -> None:
    p = makePath(home, path, filename, createdirs=True)
    with open(p, 'w') as f: 
        f.write(str(getpid()))

def getpid() -> int:
    return os.getpid()

async def wait(t: float = 0.1) -> None:
    await sleep(t)

def exit(code: int = 0) -> None:
    os._exit(code)

def terminate(sig: int = signal.SIGTERM) -> None:
    os.kill(getpid(), sig)
