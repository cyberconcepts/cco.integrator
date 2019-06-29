'''
A web client based on asyncio and aiohttp
communicating with the top-level actor (dispatcher).

2019-06-27 helmutm@cy55.de
'''

from aiohttp import ClientSession

from cco.integrator.mailbox import receive, send
from cco.integrator.message import no_message, quit
from cco.integrator.registry import getHandler, declare_handlers


async def start(ctx):
    url = ctx.config.get('server-url')
    session = ClientSession()
    ctx.state = session
    # await do_listen(ctx)
    listen = getHandler(ctx, 'listen')
    await listen(ctx)
    await session.close()

async def action(ctx, msg):
    if  msg is quit:
        return False
    url = ctx.config.get('server-url') + msg.payload.get('path', '/')
    session = ctx.state
    async with session.get((url)) as resp:
        msg = await resp.json()
        ctx.logger.debug('%s response: %s' % (ctx.pname, msg))
    #print('***', resp)
    return True


#*** register_handlers ***

def register_handlers(reg):
    declare_handlers(
            [start, action], 
            'client.web', reg)
