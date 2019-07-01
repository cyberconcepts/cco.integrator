'''
Basic actor stuff: starting an actor and communicating wit it.
  
2019-05-26 helmutm@cy55.de

'''

from importlib import import_module
import sys

from cco.integrator import context, process, registry
from cco.integrator.mailbox import receive, send
from cco.integrator.message import quit
from cco.integrator.registry import getHandler, declare_handlers


def run(pctx, name):
    ctx = setup(pctx, name)
    start = getHandler(ctx, 'start')
    p = process.run(start, ctx, name)
    pctx.children.append((p, ctx.mailbox))

def setup(pctx, name):
    conf = pctx.config.get(name, {})
    ctx = context.setupChild(pctx, conf)
    ctx.pname = name
    pctx.services.setdefault('actors', {})[name] = ctx.mailbox
    ctx.logger.debug('starting actor %s; config=%s.' % (name, conf))
    return ctx

async def start(ctx):
    listen = getHandler(ctx, 'listen')
    await listen(ctx)

async def listen(ctx):
    step = getHandler(ctx, 'step')
    while await step(ctx):
        pass
    ctx.logger.info('%s finished' % ctx.pname)

async def step(ctx):
    msg = await receive(ctx.mailbox)
    ctx.logger.debug('%s recv: msg=%s.' % (ctx.pname, msg))
    action = getHandler(ctx, 'action')
    return await action(ctx, msg)

async def action(ctx, msg):
    if  msg is quit:
        # TODO: use getHandler(ctx, 'do_quit')
        fct = do_quit
        cfg = None
    else:
        cmd = msg.payload.get('command') or '???'
        cfg = ctx.config.get('actions', {}).get(cmd, {})
        if not cfg:
            fct = do_ignore
        else:
            fct = getHandler(ctx, cfg.get('handler'), cfg.get('group'))
    res = await fct(ctx, cfg, msg)
    return res

# message/action handlers

async def do_ignore(ctx, cfg, msg):
    return True

async def do_quit(ctx, cfg, msg):
    for (p, mb) in ctx.children:
        if p.task.done():
            ctx.logger.warn('Task %s already finished' % p.name)
        else:
            await send(mb, quit)
    return False

#*** register_handlers ***

def register_handlers(reg):
    declare_handlers(
            [run, start, listen, step, action, do_ignore, do_quit], 
            'actor', reg)
