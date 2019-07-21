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
    await engine.run(tests, init, home=home)

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
    engine.Test(test00, 'config-t0.yaml'),
    engine.Test(test01, 'config-t1.yaml'),
]


# init / setup, teardown / finish

async def init():
    loadLoggerConf(home, 'logging.yaml')
    prepareFiles()

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
