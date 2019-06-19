'''
Tests for the 'cco.integrator' package.

2019-06-19 helmutm@cy55.de
'''

from collections import deque
from os.path import abspath, dirname, join
import os
import re
import shutil

from cco.integrator import context, dispatcher, system
from cco.integrator.testing.logger import loggerQueue

home = dirname(abspath(__file__))


def run():
    prepareFiles()
    ctx = context.setup(
            system='linux', home=home, cfgname='config.yaml')
    dispatcher.run(ctx)

    system.wait()
    checkEqual(len(ctx.children), 3, 1)
    # checkForSet(tc, checkLogMessage, patterns, loggerQueue)
    lr = loggerQueue.popleft()
    checkRegex(lr.msg % lr.args, r'starting actor check-dir.*', 2)
    lr = loggerQueue.popleft()
    checkRegex(lr.msg % lr.args, r'starting actor worker.*', 3)
    lr = loggerQueue.popleft()
    if lr.msg % lr.args == 'listening.':
        lr = loggerQueue.popleft()
    checkRegex(lr.msg % lr.args, r"msg={'message': .*}.", 4)

    for (p, mb) in ctx.children:
        if mb:
            mb.put('quit')
    ctx.mailbox.put('quit')
    system.wait()
    system.exit()

# testing functions

def checkEqual(vc, vx, n):
    if vc == vx:
        print 'test %02i OK' % n
    else:
        print 'test %02i failed: %s != %s' % (n, vc, vx)

def checkRegex(vc, pattern, n):
    vx = re.compile(pattern)
    if vx.search(vc):
        print 'test %02i OK' % n
    else:
        print 'test %02i failed: %s does not match %s' % (n, vc, pattern)

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
