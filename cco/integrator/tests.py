'''
Tests for the 'cco.webapi' package.

2019-06-10 helmutm@cy55.de
'''

from unittest import TestCase

from collections import deque
import os
from os.path import abspath, dirname, join
import shutil
import time

from cco.integrator import context, dispatcher

home = join(dirname(abspath(__file__)), 'testing')

loggerQueue = deque()


class Test(TestCase):
    "Basic tests."

    def setUp(self):
        prepareFiles()
        loggerQueue.clear()
        self.context = context.setup(
                system='linux', home=home, cfgname='config.yaml')
        dispatcher.run(self.context)

    def tearDown(self):
        for (p, mb) in self.context.children:
            if mb:
                mb.put('quit')
        self.context.mailbox.put('quit')
        wait()

    def testBasicStuff(self):
        wait()
        self.assertEqual(len(self.context.children), 2)
        lr = loggerQueue.popleft()
        self.assertRegexpMatches(lr.msg % lr.args, r'starting actor check-dir.*')
        lr = loggerQueue.popleft()
        self.assertRegexpMatches(lr.msg % lr.args, r'starting actor worker.*')
        lr = loggerQueue.popleft()
        if lr.msg % lr.args == 'listening.':
            lr = loggerQueue.popleft()
        self.assertRegexpMatches(lr.msg % lr.args, r"msg={'message': .*}.")


def prepareFiles():
    fn = 'test.txt'
    dataDir = join(home, 'data')
    targetDir = join(dataDir, 'target')
    backupDir = join(dataDir, 'backup')
    shutil.copy2(join(targetDir, fn), dataDir)
    os.remove(join(targetDir, fn))
    os.remove(join(backupDir, fn))

def wait(t=0.1):
    time.sleep(t)


if __name__ == '__main__':
    unittest.main()
