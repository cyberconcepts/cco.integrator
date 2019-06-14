'''
Tests for the 'cco.webapi' package.

2019-06-10 helmutm@cy55.de
'''

from unittest import TestCase

from collections import deque
from os.path import abspath, dirname, join
import time

from cco.integrator import context, dispatcher

home = join(dirname(abspath(__file__)), 'testing')

loggerQueue = deque()


class Test(TestCase):
    "Basic tests."

    def setUp(self):
        loggerQueue.clear()
        self.context = context.setup(
                system='linux', home=home, cfgname='config.yaml')
        dispatcher.startThread(self.context)

    def tearDown(self):
        self.context.mailbox.put('quit')
        for (p, mb) in self.context.children:
            if mb:
                mb.put('quit')
        wait()

    def testBasicStuff(self):
        wait()
        lr = loggerQueue.popleft()
        self.assertEqual(lr.msg % lr.args, 'listening.')


def wait(t=0.1):
    time.sleep(t)


if __name__ == '__main__':
    unittest.main()
