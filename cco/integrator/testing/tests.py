'''
Tests for the 'cco.integrator' package.

2019-06-19 helmutm@cy55.de
'''

from glob import glob
from os.path import abspath, basename, dirname, join
import os
import shutil

from cco.integrator import context, dispatcher, registry, system
from cco.integrator.mailbox import send
from cco.integrator.message import quit
from cco.integrator.testing import engine
from cco.integrator.testing.logger import loggerQueue

home = dirname(abspath(__file__))


def run():
    prepareFiles()
    te, ctx = setup('config-t0.yaml')
    engine.runTest(test00, te, ctx)
    finish([ctx])

# tests

def test00(te, ctx):
    te.checkEqual(len(ctx.children), 3)
    logMsgs = [lr.msg % lr.args for lr in loggerQueue]
    te.checkRegexAny(logMsgs, r'starting actor check-dir.*')
    te.checkRegexAny(logMsgs, r'starting actor worker.*')
    te.checkRegexAny(logMsgs, r'starting actor webserver.*')
    te.checkRegexAny(logMsgs, r".* payload={.*'command': .*}.")
    te.checkFiles(join(home, 'data', 'target'), ['test.txt'])
    te.show()

# setup, teardown / finish

def setup(cfgname='config.yaml'):
    te = engine.init()
    reg = registry.load()
    ctx = context.setup(
            system='linux', home=home, cfgname=cfgname, registry=reg)
    dispatcher.run(ctx)
    system.wait()
    return (te, ctx)

def finish(contexts):
    for ctx in contexts:
        send(ctx.mailbox, quit)
    system.wait()
    system.exit()

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
