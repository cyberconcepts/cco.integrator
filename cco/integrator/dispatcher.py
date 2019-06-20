'''
Dispatcher functions
  
2019-05-26 helmutm@cy55.de
'''

from threading import Thread

from cco.integrator import actor, context


def run(ctx, name='dispatcher'):
    p = Thread(target=start, args=[ctx])
    p.start()
    return (p, ctx.mailbox)

def start(ctx):
    start_actors(ctx)
    listen(ctx)

def listen(ctx):
    while step(ctx):
        pass

def step(ctx):
    msg = ctx.mailbox.get()
    ctx.logger.debug('msg=%s.' % msg)
    if msg == 'quit':
        for (p, mb) in ctx.children:
            mb.put('quit')
        return False
    if isinstance(msg, dict):
        target = msg.get('actor')
        if target is None:
            ctx.logger.warn('No target actor in message.')
        else:
            mb = ctx.services.get('actors', {}).get(target)
            if mb is None:
                ctx.logger.warn('Actor %s missing in services.' % target)
            else:
                mb.put(msg)
    return True


def start_actors(ctx):
    for act in ctx.config.get('actors', []):
        actor.run(ctx, act)

