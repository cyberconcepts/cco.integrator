'''
A simple testing engine, 
i.e. a set of classes and functions for 
running tests and for collecting and presenting test results

2019-06-19 helmutm@cy55.de
'''

from dataclasses import dataclass, field
from glob import glob
from os.path import abspath, basename, dirname, join
import re
import traceback

from cco.integrator import config, context, dispatcher, registry, system
from cco.integrator.mailbox import send
from cco.integrator.message import Message, dataMT, quit
from cco.integrator.testing.logger import loggerQueue

from typing import Any, Callable, Collection, Coroutine, List
from typing import Match, Optional, TypeVar, Union

Context = context.Context
TestFct = Callable[['Test', Context], Coroutine[Any, Any, None]]
T = TypeVar('T')

home: str = dirname(abspath(__file__))


# test engine

@dataclass
class Result:

    text: str

    def __str__(self) -> str:
        return self.text

ok = Result('OK')
failed = Result('failed')


@dataclass
class Item:

    number: int
    message: str
    result: Result

    def show(self) -> None:
        print('test %02i %s %s' % (self.number, self.result, 
                    self.message and ': ' + self.message or ''))


class Test:

    def __init__(self, 
                 fct: TestFct, 
                 cfgname: str = 'config.yaml', 
                 loggername: str = 'logging.yaml', 
                 name: Optional[str] = None) -> None:
        self.cfgname = cfgname
        self.loggername = loggername
        self.fct = fct
        self.name = name or fct.__name__
        self.count = 0
        self.nok = self.nfailed = 0
        self.items: List[Item] = []

    def show(self) -> None:
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

    def checkCond(self, cond: Union[bool, Optional[Match[str]]], 
                  msg: Optional[str] = None) -> None:
        if not cond:
            if msg is None:
                msg = 'condition false'
            return self.setFailed(msg)
        self.setOK()

    def checkEqual(self, vc: T, vx: T) -> None:
        self.checkCond(vc == vx, '%r != %r' % (vc, vx))

    def checkRegex(self, vc: str, pattern: str) -> None:
        vx = re.compile(pattern)
        self.checkCond(vx.search(vc), '%r does not match %r' % (vc, pattern))

    def checkRegexAny(self, coll: Collection[str], pattern: str) -> None:
        vx = re.compile(pattern)
        for vc in coll:
            if vx.search(vc):
                return self.setOK()
        self.setFailed('pattern %r not found in collection\n%s' % 
                       (pattern, coll))

    def checkFiles(self, path: str, vx: List[str]) -> None:
        vc = [basename(p) for p in glob(join(path, '*'))]
        self.checkEqual(sorted(vc), sorted(vx))


    # utility methods

    def update(self, msg: str, res: Result) -> None:
        self.count += 1
        self.items.append(Item(self.count, msg, res))

    def setOK(self) -> None:
        self.update('', ok)
        self.nok += 1

    def setFailed(self, msg: str) -> None:
        self.update(msg, failed)
        self.nfailed += 1


# testing functions

async def init() -> None:
    config.loadLoggerConf(home, 'logging.yaml')

async def setup(test: Test, 
                home: str) -> Context:
    loggerQueue.clear()
    reg = registry.load()
    #config.loadLoggerConf(home, test.loggername)
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



