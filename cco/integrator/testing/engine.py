'''
A simple testing engine, 
i.e. a set of classes and functions for 
running tests and for collecting and presenting test results

2019-06-19 helmutm@cy55.de
'''

from glob import glob
from os.path import abspath, basename, dirname, join
import re
import traceback

from cco.integrator import context, dispatcher, registry, system
from cco.integrator.mailbox import send
from cco.integrator.message import Message, dataMT, quit

home = dirname(abspath(__file__))


async def init():
    pass

async def setup(cfgname='config.yaml', home=home, name='???'):
    te = create_engine(name)
    reg = registry.load()
    ctx = context.setup(
            system='linux', home=home, cfgname=cfgname, registry=reg)
    dispatcher.run(ctx)
    await system.wait()
    return (te, ctx)

def teardown(te, ctx):
    pass

async def finish(contexts):
    await system.wait()
    for ctx in contexts:
        await send(ctx.mailbox, quit)
    await system.wait()

async def runTest(fct, eng, ctx):
    #try:
    await fct(eng, ctx)
    #except:
    #    eng.show()
    #    print(traceback.format_exc())

async def run(tests, init=init, setup=setup, teardown=teardown, finish=finish,
              home=home):
    await init()
    ctxs = []
    for test in tests:
        te, ctx = await setup(test.cfgname, home, test.name)
        ctxs.append(ctx)
        await runTest(test.fct, te, ctx)
        te.show()
        teardown(te, ctx)
    await finish(ctxs)


class Test:

    def __init__(self, cfgname, fct, name=None):
        self.cfgname = cfgname
        self.fct = fct
        self.name = name or fct.__name__

# test engine

def create_engine(name='???'):
    return Engine(name)

class Engine:

    def __init__(self, name):
        self.name = name
        self.count = 0
        self.nok = self.nfailed = 0
        self.items = []

    def show(self):
        for item in self.items:
            if item.result == failed:
                item.show()
        if self.nfailed:
            print('%s tests out of %s failed!' % (self.nfailed, self.count))
        print('%s: %s tests run.' % (self.name, self.count))

    # check methods

    def checkCond(self, cond, msg=None):
        if not cond:
            if msg is None:
                msg = 'condition false'
            return self.setFailed(msg)
        self.setOK()

    def checkEqual(self, vc, vx):
        self.checkCond(vc == vx, '%s != %s' % (vc, vx))

    def checkRegex(self, vc, pattern):
        vx = re.compile(pattern)
        self.checkCond(vx.search(vc), '%s *does not match* %s' % (vc, pattern))

    def checkRegexAny(self, coll, pattern):
        vx = re.compile(pattern)
        for vc in coll:
            if vx.search(vc):
                return self.setOK()
        self.setFailed('pattern %s not found in collection\n%s' % 
                       (pattern, coll))

    def checkFiles(self, path, vx):
        vc = [basename(p) for p in glob(join(path, '*'))]
        self.checkEqual(sorted(vc), sorted(vx))


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
        print('test %02i %s %s' % (self.number, self.result, 
                    self.message and ': ' + self.message or ''))


class Result(object):

    def __init__(self, text):
        self.text = text

    def __str__(self):
        return self.text

ok = Result('OK')
failed = Result('failed')
