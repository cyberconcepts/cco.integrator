'''
Basic actor stuff: starting an actor and communicating wit it.
  
2019-05-26 helmutm@cy55.de

'''

from importlib import import_module
import sys
from threading import Thread

from cco.integrator import context, process, registry
from cco.integrator.mailbox import receive, send
from cco.integrator.message import quit

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
    msg = receive(ctx.mailbox)
    return action(ctx, msg)

def action(ctx, msg):
    if  msg is quit:
        fct = do_quit
        cfg = None
    else:
        cmd = msg.payload.get('command') or '???'
        cfg = ctx.config.get('actions', {}).get(cmd, {})
        if not cfg:
            fct = do_ignore
        else:
            fct = getHandler(ctx, cfg.get('handler'), cfg.get('module'))
    return fct(ctx, cfg, msg)

# message/action handlers

def do_ignore(ctx, cfg, msg):
    return True

def do_quit(ctx, cfg, msg):
    for (p, mb) in ctx.children:
        send(mb, quit)
    return False

# handler registration

def register_handlers(reg):
    registry.declare_handlers(
            [run, start, listen, step, action, do_ignore, do_quit], 
            'actor', reg)

# utility functions

def getHandler(ctx, name, modSpec=None, group=None):
    handler = registry.get_handler(ctx, name, group)
    if handler is None:
        return getHandlerFromModule(ctx, name, modSpec)
    return handler

def getHandlerFromModule(ctx, name, modSpec=None):
    modSpec = modSpec or ctx.config.get('module')
    module = modSpec and import_module(modSpec) or this_module
    fname = ctx.config.get(name, name)
    return getattr(module, fname, None) or getattr(this_module, fname)
