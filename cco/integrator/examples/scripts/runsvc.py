#!bin/run

'''
Application Integrator start script (generic version):

2019-04-13 helmutm@cy55.de

'''

import asyncio
from os.path import abspath, dirname

from cco.integrator import startup
# register plugins:
from cco.integrator import actor, checker, worker
import cco.integrator.client.web
import cco.integrator.server.web
# import some.package

home = abspath(dirname(dirname(__file__)))


if __name__ == '__main__':
    asyncio.run(startup.start(home))
