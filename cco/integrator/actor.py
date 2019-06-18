'''
Basic actor stuff: starting an actor and communicating wit it.
  
2019-05-26 helmutm@cy55.de

'''

from importlib import import_module
import sys
from threading import Thread

from cco.integrator import context

this_module = sys.modules[__name__]


def run(pctx, name):
    conf = pctx.config.get(name, {})
    ctx = context.setupChild(pctx, conf)
    ctx.logger.debug('starting actor %s; config=%s.' % (name, conf))
    p = Thread(target=getFunction(ctx, 'start'), args=[ctx])
    pctx.children.append((p, ctx.mailbox))
    p.start()


def start(ctx):
    listen = getFunction(ctx, 'listen')
    listen(ctx)

def listen(ctx):
    step = getFunction(ctx, 'step')
    while step(ctx):
        pass

def step(ctx):
    msg = ctx.mailbox.get()
    return action(ctx, msg)


def do_default(ctx, cfg):
    return True

def do_quit(ctx, cfg):
    for (p, mb) in ctx.children:
        mb.put('quit')
    return False

def move_file(ctx, cfg):
    pass

def action(ctx, msg):
    cfg = ctx.get('actions', {}).get(msg, {})
    if not cfg:
        if  msg == 'quit':
            fct = do_quit
        else:
            fct = do_default
    else:
        fname = cfg.get('function')
        modSpec = cfg.get('module')
        fct = getFunction(ctx, fname, modSpec)
    return fct(ctx, cfg)

def getFunction(ctx, name, modSpec=None):
    modSpec = modSpec or ctx.config.get('module')
    module = modSpec and import_module(modSpec) or this_module
    fname = ctx.config.get(name, name)
    return getattr(module, fname, None) or getattr(this_module, fname)
