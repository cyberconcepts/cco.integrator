'''
Tests for the 'cco.webapi' package.

2019-06-10 helmutm@cy55.de
'''

import unittest

from os.path import abspath, dirname, join
import time

from cco.integrator import dispatcher

home = join(dirname(abspath(__file__)), 'testing')


class Test(unittest.TestCase):
    "Basic tests."

    def setUp(self):
        self.mailbox = dispatcher.init()
        self.actors = dispatcher.startThread(
                self.mailbox, 
                dict(system='linux', home=home, config='config.yaml'))

    def tearDown(self):
        time.sleep(1)
        for (p, mb) in self.actors:
            if mb:
                mb.put('quit')
        time.sleep(1)

    def testBasicStuff(self):
        pass


if __name__ == '__main__':
    unittest.main()
