#!bin/run

'''
Run tests for the 'cco.integrator' package.

2019-06-19 helmutm@cy55.de
'''

import asyncio

from cco.integrator.testing import tests

# register plugins:
from cco.integrator import checker, worker
import cco.integrator.client.web
import cco.integrator.server.web


if __name__ == '__main__':
    asyncio.run(tests.run())#, debug=True)
