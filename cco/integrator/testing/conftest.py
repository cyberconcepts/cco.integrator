'''
Common pytest configuration and fixtures.

2019-11-06 helmutm@cy55.de
'''

import asyncio
import pytest
from cco.integrator import config
from cco.integrator.testing.common import \
            base_setup, contexts, home, prepareFiles


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
def make_context(integrator_base):
    async def start_integrator(cfgname):
        ctx = await base_setup(cfgname)
        contexts.append(ctx)
        return ctx
    return start_integrator

