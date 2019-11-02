'''
Tests for the 'cco.integrator' package for use with pytest.

2019-11-02 helmutm@cy55.de
'''

from glob import glob
from os.path import abspath, basename, dirname, join
import os
import shutil

from cco.integrator import config, context, dispatcher, registry, system
from cco.integrator.mailbox import send
from cco.integrator.message import Message, dataMT, quit
from cco.integrator.testing.logger import loggerQueue

import pytest

from typing import Collection, List

Context = context.Context

home: str = dirname(abspath(__file__))


# fixture stuff

@pytest.fixture(scope='module')
def integrator_base():
    pass

@pytest.fixture
def make_context(request):
    contexts = []
    async def stop_integrator():
        for ctx in contexts:
            await base_teardown(ctx)
    async def start_integrator(cfgname):
        ctx = await base_setup(cfgname)
        contexts.append(ctx)
        request.addfinalizer(stop_integrator)
        return ctx
        #yield ctx
        #await base_teardown(ctx)
    return start_integrator


async def base_setup(cfgname):
    reg = registry.load()
    config.loadLoggerConf(home, 'logging.yaml')
    ctx = context.setup(
            system='test', home=home, cfgname=cfgname, registry=reg)
    dispatcher.run(ctx)
    await system.wait()
    return ctx

async def base_teardown(ctx):
    print('teardown')
    await send(ctx.mailbox, quit)


# tests

@pytest.mark.asyncio
async def test_0(integrator_base):
    ctx = await base_setup('config-t0.yaml')
    #ctx = make_context('config-t0.yaml')
    assert len(ctx.children) == 3
    await base_teardown(ctx)

@pytest.mark.asyncio
async def test_1(make_context, integrator_base):
    ctx = await make_context('config-t1.yaml')
    assert len(ctx.children) == 1
    #ctx = await base_setup('config-t1.yaml')
    await base_teardown(ctx)


# utilities

def checkRegexAny(coll: Collection[str], pattern: str) -> bool:
    vx = re.compile(pattern)
    for vc in coll:
        if vx.search(vc):
            return True
    return False
    #self.setFailed('pattern %r not found in collection\n%s' % 
    #               (pattern, coll))

def checkFiles(path: str, vx: List[str]) -> bool:
    vc = [basename(p) for p in glob(join(path, '*'))]
    return sorted(vc) == sorted(vx)

