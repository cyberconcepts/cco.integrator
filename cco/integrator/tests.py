'''
Tests for the 'cco.integrator' package.

2019-06-10 helmutm@cy55.de
'''

from unittest import TestCase

from collections import deque
from os.path import abspath, dirname, join
import os
import shutil

from cco.integrator import context, dispatcher, system
from cco.integrator.testing.logger import loggerQueue

home = join(dirname(abspath(__file__)), 'testing')


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
        system.wait()
        system.exit()

    def test02_check(self):
        system.wait()
        self.assertEqual(len(self.context.children), 3)
        lr = loggerQueue.popleft()
        self.assertRegexpMatches(lr.msg % lr.args, r'starting actor check-dir.*')
        lr = loggerQueue.popleft()
        self.assertRegexpMatches(lr.msg % lr.args, r'starting actor worker.*')
        lr = loggerQueue.popleft()
        if lr.msg % lr.args == 'listening.':
            lr = loggerQueue.popleft()
        self.assertRegexpMatches(lr.msg % lr.args, r"msg={'message': .*}.")


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


if __name__ == '__main__':
    unittest.main()
