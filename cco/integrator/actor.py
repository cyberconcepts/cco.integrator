'''
Basic actor stuff: starting an actor and communicating wit it.
  
2019-05-26 helmutm@cy55.de

'''

from importlib import import_module
import sys
from threading import Thread

from cco.integrator import context

this_module = sys.modules[__name__]


def run(pctx, actor):
    conf = pctx.config.get(actor, {})
    ctx = context.setupChild(pctx, conf)
    ctx.logger.debug('starting actor %s; config=%s.' % (actor, conf))
    p = Thread(target=getFunction(ctx, 'start'), args=[ctx])
    pctx.children.append((p, ctx.mailbox))
    p.start()


def start(ctx):
    listener = getFunction(ctx, 'listener')
    listener(ctx)

def listener(ctx):
    step = getFunction(ctx, 'step')
    while step(ctx):
        pass

def step(ctx):
    msg = ctx.mailbox.get()
    if msg is not None:
        ctx.parent_mb.put(msg)
    return msg != 'quit'


def getFunction(ctx, name):
    modSpec = ctx.config.get('module')
    module = modSpec and import_module(modSpec) or this_module
    fname = ctx.config.get(name, name)
    return getattr(module, fname, getattr(this_module, fname))
