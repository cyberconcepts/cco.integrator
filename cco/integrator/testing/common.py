'''
Common stuff for cco.integrator tests with pytes.

2019-11-06 helmutm@cy55.de
'''

from glob import glob
from os.path import abspath, basename, dirname, join
import os
import re
import shutil

from cco.integrator import context, dispatcher, registry, system
from cco.integrator.mailbox import send
from cco.integrator.message import quit
from cco.integrator.testing.logger import loggerQueue

from typing import Collection, List

Context = context.Context

home: str = dirname(abspath(__file__))
contexts: List[Context] = []


# setup and teardown stuff

async def base_setup(cfgname: str) -> Context:
    reg = registry.load()
    ctx = context.setup(
            system='test', home=home, cfgname=cfgname, registry=reg)
    dispatcher.run(ctx)
    await system.wait()
    contexts.append(ctx)
    return ctx

async def stop_actors() -> None:
    for ctx in contexts:
        await send(ctx.mailbox, quit)
        await system.wait()

def prepareFiles() -> None:
    dataDir = join(home, 'data')
    targetDir = join(dataDir, 'target')
    backupDir = join(dataDir, 'backup')
    filenames = glob(join(targetDir, '*'))
    for fn in filenames:
        try:
            fn = basename(fn)
            shutil.copy2(join(targetDir, fn), dataDir)
            os.remove(join(targetDir, fn))
            os.remove(join(backupDir, fn))
        except IOError:
            pass


# checks for use in assert statements

def checkRegexAny(coll: Collection[str], pattern: str) -> bool:
    vx = re.compile(pattern)
    for vc in coll:
        if vx.search(vc):
            return True
    return False

def checkLogs(pattern: str) -> bool:
    logMsgs = [lr.msg % lr.args for lr in loggerQueue]
    return checkRegexAny(logMsgs, pattern)

def checkFiles(path: str, vx: List[str]) -> bool:
    vc = [basename(p) for p in glob(join(path, '*'))]
    return sorted(vc) == sorted(vx)

