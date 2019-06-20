'''
Tests for the 'cco.integrator' package.

2019-06-19 helmutm@cy55.de
'''

from collections import deque
from os.path import abspath, dirname, join
import os
import shutil

from cco.integrator import context, dispatcher, system
from cco.integrator.testing import engine
from cco.integrator.testing.logger import loggerQueue

home = dirname(abspath(__file__))


def run():
    # setup
    te = engine.init()
    prepareFiles()
    ctx = context.setup(
            system='linux', home=home, cfgname='config.yaml')
    dispatcher.run(ctx)

    # test
    engine.runTest(test, te, ctx)

    # finish
    ctx.mailbox.put('quit')
    system.wait()
    te.show()
    system.exit()

def test(te, ctx):
    system.wait()
    te.checkEqual(len(ctx.children), 3)
    # te.checkForSet(te.checkLogMessage, patterns, loggerQueue)
    lr = loggerQueue.popleft()
    te.checkRegex(lr.msg % lr.args, r'starting actor check-dir.*')
    lr = loggerQueue.popleft()
    te.checkRegex(lr.msg % lr.args, r'starting actor worker.*')
    lr = loggerQueue.popleft()
    te.checkRegex(lr.msg % lr.args, r'starting actor webserver.*')
    lr = loggerQueue.popleft()
    te.checkRegex(lr.msg % lr.args, r"msg={'message': .*}.")

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
