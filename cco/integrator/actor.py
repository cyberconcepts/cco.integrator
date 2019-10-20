'''
Basic actor stuff: starting an actor and communicating wit it.
  
2019-05-26 helmutm@cy55.de

'''

from importlib import import_module
import sys

from cco.integrator.config import Config
from cco.integrator import context, process, registry
from cco.integrator.mailbox import receive, send
from cco.integrator.message import quit, Message
from cco.integrator.registry import getHandler, declare_handlers

from typing import cast, Dict, Optional

Context = context.Context
Registry = registry.Registry


def run(pctx: Context, name: str) -> None:
    ctx = setup(pctx, name)
    start = getHandler(ctx, 'start')
    if start is None:
        ctx.logger.warn('start handler for %s not found' % name)
    else:
        p = process.run(start, ctx, name)
        pctx.children.append((p, ctx.mailbox))

def setup(pctx: Context, name: str) -> Context:
    conf = cast(Config, pctx.config.get(name, {}))
    ctx = context.setupChild(pctx, conf)
    ctx.pname = name
    pctx.services.setdefault('actors', {})[name] = ctx.mailbox
    ctx.logger.debug('starting actor %s; config=%s.' % (name, conf))
    return ctx

async def start(ctx: Context) -> None:
    listen = getHandler(ctx, 'listen')
    if listen is None:
        ctx.logger.warn('listen handler for %s not found' % ctx.pname)
    else:
        await listen(ctx)

async def listen(ctx: Context) -> None:
    step = getHandler(ctx, 'step')
    if step is None:
        ctx.logger.warn('step handler for %s not found' % ctx.pname)
    else:
        while await step(ctx):
            pass
    ctx.logger.info('%s finished' % ctx.pname)

async def step(ctx: Context) -> bool:
    msg = await receive(ctx.mailbox)
    ctx.logger.debug('%s recv: msg=%s.' % (ctx.pname, msg))
    action = getHandler(ctx, 'action')
    if action is None:
        ctx.logger.warn('action handler for %s not found' % ctx.pname)
        return False
    else:
        return await action(ctx, msg)

async def action(ctx: Context, msg: Message) -> bool:
    # TODO: get handler/action using message type
    if  msg is quit:
        # TODO: use getHandler(ctx, 'do_quit')
        fct = do_quit
        cfg = None
    else:
        cmd = msg.payload.get('command') or '???'
        actions = ctx.config.get('actions', {})
        cfg = cast(Dict, isinstance(actions, dict) and actions.get(cmd, {}))
        if not cfg:
            fct = do_ignore
        else:
            handler = cast(str, cfg.get('handler'))
            group = cast(str, cfg.get('group'))
            hdl = getHandler(ctx, handler, group)
            if hdl is None:
                ctx.logger.warn('Handler not found, config is: %s' % cfg)
                fct = do_quit
            else:
                fct = hdl
    res = await fct(ctx, cfg, msg)
    return res

# message/action handlers

async def do_ignore(ctx: Context, cfg: Optional[Config], msg: Message) -> bool:
    return True

async def do_quit(ctx: Context, cfg: Optional[Config], msg: Message) -> bool:
    for (p, mb) in ctx.children:
        if p.task.done():
            ctx.logger.warn('Task %s already finished' % p.name)
        else:
            await send(mb, quit)
    return False

#*** register_handlers ***

def register_handlers(reg: Registry) -> None:
    declare_handlers(
            [run, start, listen, step, action, do_ignore, do_quit], 
            'actor', reg)
