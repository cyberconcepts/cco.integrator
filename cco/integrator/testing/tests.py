'''
Tests for the 'cco.integrator' package.

2019-06-19 helmutm@cy55.de
'''

from glob import glob
from os.path import abspath, basename, dirname, join
import os
import shutil

from cco.integrator.config import loadLoggerConf
from cco.integrator import context, dispatcher, registry, system
from cco.integrator.mailbox import send
from cco.integrator.message import Message, dataMT, quit
from cco.integrator.testing import engine
from cco.integrator.testing.logger import loggerQueue

home = dirname(abspath(__file__))


async def run():
    loadLoggerConf(home, 'logging.yaml')
    prepareFiles()
    ctxs = []
    for cfgname, test in tests:
        te, ctx = await setup(cfgname)
        ctxs.append(ctx)
        await engine.runTest(test, te, ctx)
        te.show()
        teardown(te, ctx)
    await finish(ctxs)

# tests

async def test00(te, ctx):
    te.checkEqual(len(ctx.children), 3)
    logMsgs = [lr.msg % lr.args for lr in loggerQueue]
    te.checkRegexAny(logMsgs, r'starting actor check-dir.*')
    te.checkRegexAny(logMsgs, r'starting actor worker.*')
    te.checkRegexAny(logMsgs, r'starting actor webserver.*')
    te.checkRegexAny(logMsgs, r".* payload={.*'command': .*}.")
    te.checkFiles(join(home, 'data', 'target'), ['test.txt'])

async def test01(te, ctx):
    te.checkEqual(len(ctx.children), 1)
    (p, mb) = ctx.children[0]
    await send(mb, Message(dict(value='dummy'), dataMT))


tests = [
    ('config-t0.yaml', test00),
    ('config-t1.yaml', test01),
]


# setup, teardown / finish

async def setup(cfgname='config.yaml'):
    te = engine.init()
    reg = registry.load()
    ctx = context.setup(
            system='linux', home=home, cfgname=cfgname, registry=reg)
    dispatcher.run(ctx)
    #await dispatcher.start(ctx)
    await system.wait()
    return (te, ctx)

def teardown(te, ctx):
    pass

async def finish(contexts):
    await system.wait()
    for ctx in contexts:
        await send(ctx.mailbox, quit)
    await system.wait()
    #for rec in loggerQueue:
    #    print(rec)
    #system.exit()

# utilities

def prepareFiles():
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
