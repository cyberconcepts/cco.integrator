'''
Tests for the 'cco.integrator' package.

2019-06-19 helmutm@cy55.de
'''

from os.path import abspath, dirname, join
import os
import shutil

from cco.integrator import context, dispatcher, registry, system
from cco.integrator.mailbox import send
from cco.integrator.message import quit
from cco.integrator.testing import engine
from cco.integrator.testing.logger import loggerQueue

home = dirname(abspath(__file__))


def run():
    te, ctx = setup()
    engine.runTest(test01, te, ctx)
    finish(te, ctx)

# tests

def test01(te, ctx):
    te.checkEqual(len(ctx.children), 3)
    logMsgs = [lr.msg % lr.args for lr in loggerQueue]
    te.checkRegexAny(logMsgs, r'starting actor check-dir.*')
    te.checkRegexAny(logMsgs, r'starting actor worker.*')
    te.checkRegexAny(logMsgs, r'starting actor webserver.*')
    te.checkRegexAny(logMsgs, r".* payload={'command': .*}.")

# setup, teardown / finish

def setup():
    te = engine.init()
    prepareFiles()
    reg = registry.load()
    ctx = context.setup(
            system='linux', home=home, cfgname='config.yaml', registry=reg)
    dispatcher.run(ctx)
    system.wait()
    return (te, ctx)

def finish(te, ctx):
    send(ctx.mailbox, quit)
    system.wait()
    te.show()
    system.exit()

# utilities

def prepareFiles():
    fn = 'test.txt'
    dataDir = join(home, 'data')
    targetDir = join(dataDir, 'target')
    backupDir = join(dataDir, 'backup')
    try:
        shutil.copy2(join(targetDir, fn), dataDir)
        os.remove(join(targetDir, fn))
        os.remove(join(backupDir, fn))
    except IOError:
        pass
