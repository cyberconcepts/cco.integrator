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
        dispatcher.run(self.context)

    def tearDown(self):
        for (p, mb) in self.context.children:
            if mb:
                mb.put('quit')
        self.context.mailbox.put('quit')
        wait()

    def testBasicStuff(self):
        wait()
        self.assertEqual(len(self.context.children), 1)
        lr = loggerQueue.popleft()
        self.assertRegexpMatches(lr.msg % lr.args, r'starting actor .*')
        lr = loggerQueue.popleft()
        if lr.msg % lr.args == 'listening.':
            lr = loggerQueue.popleft()
        self.assertRegexpMatches(lr.msg % lr.args, r"msg={'action': .*}.")


def wait(t=0.1):
    time.sleep(t)


if __name__ == '__main__':
    unittest.main()
