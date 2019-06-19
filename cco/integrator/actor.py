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
    pctx.registry.setdefault('actors', {})[name] = ctx.mailbox
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


def do_default(ctx, cfg, msg):
    return True

def do_quit(ctx, cfg, msg):
    for (p, mb) in ctx.children:
        mb.put('quit')
    return False


def action(ctx, msg):
    if isinstance(msg, dict):
        message = msg.get('message') or '???'
    else:
        message = msg
    cfg = ctx.config.get('actions', {}).get(message, {})
    if not cfg:
        if  msg == 'quit':
            fct = do_quit
        else:
            fct = do_default
    else:
        fname = cfg.get('function')
        modSpec = cfg.get('module')
        fct = getFunction(ctx, fname, modSpec)
    return fct(ctx, cfg, msg)

def getFunction(ctx, name, modSpec=None):
    modSpec = modSpec or ctx.config.get('module')
    module = modSpec and import_module(modSpec) or this_module
    fname = ctx.config.get(name, name)
    return getattr(module, fname, None) or getattr(this_module, fname)
