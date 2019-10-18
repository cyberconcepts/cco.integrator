#!bin/run

'''
Application Integrator start script (generic version):

2019-04-13 helmutm@cy55.de

'''

import asyncio
from os.path import abspath, dirname

from cco.integrator import startup

home = abspath(dirname(dirname(__file__)))


if __name__ == '__main__':
    asyncio.run(startup.start(home))
