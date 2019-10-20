'''
A web server based on asyncio and aiohttp
communicating with the top-level actor (dispatcher).

2019-06-27 helmutm@cy55.de
'''

from aiohttp import web

from cco.integrator import actor
from cco.integrator.context import Context
from cco.integrator.mailbox import receive, send
from cco.integrator.message import no_message, quit
from cco.integrator.registry import getHandler, declare_handlers, Registry

from typing import Any, Dict, List


async def start(ctx: Context) -> None:
    port = ctx.config.get('port', 8123)
    app = web.Application()
    app['context'] = ctx
    routeCfgs = []
    rc1 = ctx.config.get('routes') or ['default-routes']
    for r in rc1:
        if isinstance(r, str):
            routeCfgs.extend(getPredefinedRoutes(r))
        else:
            routeCfgs.append(r)
    app['routes'] = dict((r['name'], r) for r in routeCfgs)
    routes = [web.get(rc['path'], 
                      getHandler(ctx, rc['handler']),
                      name=rc['name']) 
                for rc in routeCfgs]
    app.add_routes(routes)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', port)
    ctx.state = site
    await site.start()
    await listen(ctx)
    ctx.logger.info('%s finished' % ctx.pname)

async def listen(ctx: Context) -> None:
    while await step(ctx):
        pass

async def step(ctx: Context) -> bool:
    msg = await receive(ctx.mailbox)
    ctx.logger.debug('webserver recv: msg=%s.' % msg)
    if msg is quit:
        await stop_site(ctx)
        return await actor.do_quit(ctx, None, msg)
    return True

async def stop_site(ctx: Context) -> bool:
    site = ctx.state
    await site.stop()
    return False


def build_response(result: Dict[str, Any], msg: str) -> str:
    data = {'result': result, 'message': msg}
    return web.json_response(data)

async def do_default(request: web.Request) -> web.Response:
    ctx = request.app['context']
    name = request.match_info.route.name
    cfg = request.app['routes'][name]
    #await send(ctx.parent_mb, Message())
    return build_response('ok', name)

async def do_poll(request: web.Request) -> web.Response:
    ctx = request.app['context']
    cfg = request.app['routes'][request.match_info.route.name]
    timeout = cfg.get('timeout', 15)
    msg = await receive(ctx.parent_mb, timeout)
    if msg is no_message:
        data = ''
        result = 'idle'
    else:
        data = msg.payload # TODO: check message type
        result = 'data'
    return build_response(result, data)

async def do_quit(request: web.Request) -> web.Response:
    ctx = request.app['context']
    cfg = request.app['routes'][request.match_info.route.name]
    await send(ctx.parent_mb, quit)
    return build_response('ok', 'quit')

# helper functions

predefined_routes = {
    'default-routes': [
        dict(path='/control/quit', name='quit', handler='do_quit'),
        dict(path='/control/poll', name='poll', handler='do_poll'),
        dict(path='/event', name='event', handler='do_default')]
}

def getPredefinedRoutes(r: str) -> List[Dict[str, str]]:
    return predefined_routes.get(r) or []


#*** register_handlers ***

def register_handlers(reg: Registry) -> None:
    declare_handlers(
            [start, do_default, do_poll, do_quit], 
            'server.web', reg)
