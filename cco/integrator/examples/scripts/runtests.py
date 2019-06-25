'''
Run tests for the 'cco.integrator' package.

2019-06-19 helmutm@cy55.de
'''

import asyncio

from cco.integrator.testing import tests

if __name__ == '__main__':
    asyncio.run(tests.run())
