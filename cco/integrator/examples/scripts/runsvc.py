'''
Application Integrator (Linux version):
  
2019-04-13 helmutm@cy55.de

'''

import asyncio
from os.path import abspath, dirname

from cco.integrator import system

home = abspath(dirname(dirname(__file__)))


if __name__ == '__main__':
    params = system.cmdlineArgs()
    asyncio.run(system.start(home, **params))
