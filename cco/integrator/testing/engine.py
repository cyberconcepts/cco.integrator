'''
A simple testing engine, 
i.e. a set of classes and functions for 
checking, collecting, presenting tests

2019-06-19 helmutm@cy55.de
'''

import re
import traceback

from cco.integrator import system


def init():
    return Engine()


def runTest(fct, eng, ctx):
    try:
        fct(eng, ctx)
    except:
        eng.show()
        print traceback.format_exc()
        system.exit()


class Engine(object):

    def __init__(self):
        self.count = 0
        self.nok = self.nfailed = 0
        self.items = []

    def show(self):
        for item in self.items:
            item.show()
        if self.nfailed:
            print '%s tests of %s failed!' % (self.nfailed, self.count)

    # check methods

    def checkEqual(self, vc, vx):
        if vc != vx:
            msg = '%s != %s' % (vc, vx)
            return self.setFailed(msg)
        self.setOK()

    def checkRegex(self, vc, pattern):
        vx = re.compile(pattern)
        if not vx.search(vc):
            msg = '%s *does not match* %s' % (vc, pattern)
            return self.setFailed(msg)
        self.setOK()

    # utility methods

    def update(self, msg, res):
        self.count += 1
        self.items.append(Item(self.count, msg, res))

    def setOK(self):
        self.update('', ok)
        self.nok += 1

    def setFailed(self, msg):
        self.update(msg, failed)
        self.nfailed += 1


class Item(object):

    def __init__(self, number, message, result):
        self.number = number
        self.message = message
        self.result = result

    def show(self):
        print 'test %02i %s %s' % (self.number, self.result, 
                    self.message and ': ' + self.message or '')


class Result(object):

    def __init__(self, text):
        self.text = text

    def __str__(self):
        return self.text

ok = Result('OK')
failed = Result('failed')
