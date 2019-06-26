'''
Actors that check for some condition
  
2019-06-16 helmutm@cy55.de

'''

from glob import glob
from os.path import isfile, join

from cco.integrator.actor import do_quit
from cco.integrator.mailbox import receive, send
from cco.integrator.message import Message, commandMT, no_message, quit
from cco.integrator import registry


async def check_dir(ctx):
    timeout = ctx.config.get('receive_timeout', 15)
    path = join(ctx.home, ctx.config.get('path', '.'))
    fns = check(path)
    if fns:
        action = ctx.config.get('action', {})
        cmd = action.get('command', '???')
        act = action.get('actor', '???')
        msg = Message(dict(actor=act, command=cmd, filenames=fns), commandMT)
        ctx.logger.debug('msg=%s.' % msg)
        await send(ctx.parent_mb, msg)
    msg = await receive(ctx.mailbox, timeout)
    ctx.logger.debug('msg=%s.' % msg)
    if msg is quit:
        return await do_quit(ctx, None, msg)
    else:
        return True

def check(path):
    return [f for f in glob(join(path, '*')) if isfile(f)]


def register_handlers(reg):
    registry.declare_handlers([check_dir], 'checker', reg)

