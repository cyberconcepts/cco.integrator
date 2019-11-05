'''
Tests for the 'cco.integrator' package for use with pytest.

2019-11-02 helmutm@cy55.de
'''

import asyncio
import functools
from glob import glob
from os.path import abspath, basename, dirname, join
import os
import re
import shutil

from cco.integrator import config, context, dispatcher, registry, system
from cco.integrator.mailbox import send
from cco.integrator.message import Message, dataMT, quit
from cco.integrator.testing.logger import loggerQueue

import pytest

from typing import Collection, List

Context = context.Context

home: str = dirname(abspath(__file__))

contexts = []


# fixtures

@pytest.yield_fixture(scope='module')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
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


# the real setup and teardown stuff

async def base_setup(cfgname):
    loggerQueue.clear()
    reg = registry.load()
    #config.loadLoggerConf(home, 'logging.yaml')
    ctx = context.setup(
            system='test', home=home, cfgname=cfgname, registry=reg)
    dispatcher.run(ctx)
    await system.wait()
    return ctx

async def stop_actors():
    for ctx in contexts:
        await send(ctx.mailbox, quit)
        await system.wait()


# tests

@pytest.mark.asyncio
async def test_0(make_context):
    ctx = await make_context('config-t0.yaml')
    logMsgs = [lr.msg % lr.args for lr in loggerQueue]
    assert len(ctx.children) == 3
    assert checkRegexAny(logMsgs, r'starting actor check-dir.*')
    assert checkFiles(join(home, 'data', 'target'), ['test.txt'])

@pytest.mark.asyncio
async def test_1(make_context):
    ctx = await make_context('config-t1.yaml')
    logMsgs = [lr.msg % lr.args for lr in loggerQueue]
    assert len(ctx.children) == 1
    assert checkRegexAny(logMsgs, r'starting actor webclient.*')
    (p, mb) = ctx.children[0]
    await send(mb, Message(dict(value='dummy'), dataMT))
    await system.wait()
    logMsgs = [lr.msg % lr.args for lr in loggerQueue]
    assert checkRegexAny(logMsgs, r'dummy.*')

@pytest.mark.asyncio
async def test_z():
    await stop_actors()

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

def prepareFiles() -> None:
    dataDir = join(home, 'data')
    targetDir = join(dataDir, 'target')
    backupDir = join(dataDir, 'backup')
    filenames = glob(join(targetDir, '*'))
    for fn in filenames:
        try:
            fn = basename(fn)
            shutil.copy2(join(targetDir, fn), dataDir)
            os.remove(join(targetDir, fn))
            os.remove(join(backupDir, fn))
        except IOError:
            pass
