'''
Dispatcher functions
  
2019-05-26 helmutm@cy55.de
'''

from cco.integrator import actor, context, process
from cco.integrator.mailbox import receive, send
from cco.integrator.message import quit


def run(ctx, name='dispatcher'):
    p = process.run(start, [ctx], name)
    return (p, ctx.mailbox)

async def start(ctx):
    start_actors(ctx)
    await listen(ctx)

async def listen(ctx):
    while await step(ctx):
        pass

async def step(ctx):
    msg = await receive(ctx.mailbox)
    ctx.logger.debug('dispatcher recv: msg=%s.' % msg)
    if msg is quit:
        return await actor.do_quit(ctx, None, msg)
    target = msg.payload.get('actor')
    if target is None:
        ctx.logger.warn('No target actor in message.')
    else:
        mb = ctx.services.get('actors', {}).get(target)
        if mb is None:
            ctx.logger.warn('Actor %s missing in services.' % target)
        else:
            await send(mb, msg)
    return True


def start_actors(ctx):
    for act in ctx.config.get('actors', []):
        actor.run(ctx, act)

