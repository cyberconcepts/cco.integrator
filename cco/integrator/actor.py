'''
Basic actor stuff: starting an actor and communicating wit it.
  
2019-05-26 helmutm@cy55.de

'''

from importlib import import_module
import sys
from threading import Thread

from cco.integrator import context, mailbox, process, registry

this_module = sys.modules[__name__]


def run(pctx, name):
    conf = pctx.config.get(name, {})
    ctx = context.setupChild(pctx, conf)
    pctx.services.setdefault('actors', {})[name] = ctx.mailbox
    ctx.logger.debug('starting actor %s; config=%s.' % (name, conf))
    p = process.run(start, [ctx])
    pctx.children.append((p, ctx.mailbox))


def start(ctx):
    listen = getHandler(ctx, 'listen')
    listen(ctx)

def listen(ctx):
    step = getHandler(ctx, 'step')
    while step(ctx):
        pass

def step(ctx):
    msg = ctx.mailbox.get()
    return action(ctx, msg)

def action(ctx, msg):
    if isinstance(msg, dict):
        cmd = msg.get('command') or '???'
    else:
        cmd = msg
    cfg = ctx.config.get('actions', {}).get(cmd, {})
    if not cfg:
        if  msg == 'quit':
            fct = do_quit
        else:
            fct = do_default
    else:
        fname = cfg.get('handler')
        modSpec = cfg.get('module')
        fct = getHandler(ctx, fname, modSpec)
    return fct(ctx, cfg, msg)

# message/action handlers

def do_default(ctx, cfg, msg):
    return True

def do_quit(ctx, cfg, msg):
    for (p, mb) in ctx.children:
        mb.put('quit')
    return False

# utility functions

def getHandler(ctx, name, modSpec=None, group=None):
    group = group or ctx.config.get('group')
    if group is None or group not in ctx.registry.groups:
        return getHandlerFromModule(ctx, name, modSpec)

def getHandlerFromModule(ctx, name, modSpec=None):
    modSpec = modSpec or ctx.config.get('module')
    module = modSpec and import_module(modSpec) or this_module
    fname = ctx.config.get(name, name)
    return getattr(module, fname, None) or getattr(this_module, fname)
