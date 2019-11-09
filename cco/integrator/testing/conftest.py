'''
Common pytest configuration and fixtures.

2019-11-06 helmutm@cy55.de
'''

import asyncio
import pytest
from cco.integrator import config
from cco.integrator.testing.common import base_setup, home, prepareFiles
from cco.integrator.testing.logger import loggerQueue


@pytest.yield_fixture(scope='module')
def event_loop(request):
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope='module')
def integrator_base(event_loop):
    config.loadLoggerConf(home, 'logging.yaml')
    prepareFiles()

@pytest.fixture
def clear_logs(integrator_base):
    loggerQueue.clear()

@pytest.fixture
def make_context(clear_logs):
    async def start_integrator(cfgname):
        return await base_setup(cfgname)
    return start_integrator

