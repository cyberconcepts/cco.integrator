'''
Tests for the 'cco.integrator' package for use with pytest.

2019-11-02 helmutm@cy55.de
'''

from os.path import join

from cco.integrator import system
from cco.integrator.mailbox import send
from cco.integrator.message import Message, dataMT
from cco.integrator.testing.common import checkFiles, checkLogs, home, stop_actors

import pytest


# tests

@pytest.mark.asyncio
async def test_0(make_context):
    ctx = await make_context('config-t0.yaml')
    assert len(ctx.children) == 3
    assert checkLogs(r'starting actor check-dir')
    assert checkFiles(join(home, 'data', 'target'), ['test.txt'])

@pytest.mark.asyncio
async def test_1(make_context):
    ctx = await make_context('config-t1.yaml')
    assert len(ctx.children) == 1
    assert checkLogs(r'starting actor webclient')
    (p, mb) = ctx.children[0]
    await send(mb, Message(dict(value='dummy'), dataMT))
    await system.wait()
    assert checkLogs(r'dummy')

@pytest.mark.asyncio
async def test_z(clear_logs):
    await stop_actors()
    assert checkLogs(r'finished')

