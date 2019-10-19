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

from cco.integrator import config, context, dispatcher, registry, system
from cco.integrator.mailbox import send
from cco.integrator.message import Message, dataMT, quit

from typing import Any, Callable, Coroutine, List

Context = context.Context

home: str = dirname(abspath(__file__))


# test engine

class Test:

    def __init__(self, fct, 
                 cfgname='config.yaml', 
                 loggername='logging.yaml', 
                 name=None):
        self.cfgname = cfgname
        self.loggername = loggername
        self.fct = fct
        self.name = name or fct.__name__
        self.count = 0
        self.nok = self.nfailed = 0
        self.items = []

    def show(self):
        if self.nfailed:
            print('%s: failed tests:' % (self.name))
            for item in self.items:
                if item.result == failed:
                    item.show()
            print('%s: %s tests out of %s failed!' % 
                  (self.name, self.nfailed, self.count))
        else:
            print('%s: %s tests OK.' % (self.name, self.count))

    # check methods

    def checkCond(self, cond, msg=None):
        if not cond:
            if msg is None:
                msg = 'condition false'
            return self.setFailed(msg)
        self.setOK()

    def checkEqual(self, vc, vx):
        self.checkCond(vc == vx, '%r != %r' % (vc, vx))

    def checkRegex(self, vc, pattern):
        vx = re.compile(pattern)
        self.checkCond(vx.search(vc), '%r does not match %r' % (vc, pattern))

    def checkRegexAny(self, coll, pattern):
        vx = re.compile(pattern)
        for vc in coll:
            if vx.search(vc):
                return self.setOK()
        self.setFailed('pattern %r not found in collection\n%s' % 
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


# testing functions

async def init() -> None:
    pass

async def setup(test: Test, 
                home: str) -> Context:
    reg = registry.load()
    config.loadLoggerConf(home, test.loggername)
    ctx = context.setup(
            system='test', home=home, cfgname=test.cfgname, registry=reg)
    dispatcher.run(ctx)
    await system.wait()
    return ctx

def teardown(te: Test, ctx: Context) -> None:
    pass

async def finish(contexts: List[Context]) -> None:
    await system.wait()
    for ctx in contexts:
        await send(ctx.mailbox, quit)
    await system.wait()

async def runTest(test: Test, ctx: Context) -> None:
    #try:
    await test.fct(test, ctx)
    #except:
    #    eng.show()
    #    print(traceback.format_exc())

async def run(tests: List[Test], 
              init: Callable[[], Coroutine[Any, Any, None]] = init, 
              setup: Callable[[Test, str], Coroutine[Any, Any, Context]] = setup, 
              teardown: Callable[[Test, Context], None] = teardown, 
              finish: Callable[[List[Context]], Coroutine[Any, Any, None]] = finish,
              home: str = home) -> None:
    await init()
    ctxs = []
    for test in tests:
        ctx = await setup(test, home)
        ctxs.append(ctx)
        await runTest(test, ctx)
        test.show()
        teardown(test, ctx)
    await finish(ctxs)



