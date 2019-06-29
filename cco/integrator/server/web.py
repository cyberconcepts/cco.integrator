'''
A web server based on asyncio and aiohttp
communicating with the top-level actor (dispatcher).

2019-06-27 helmutm@cy55.de
'''

from aiohttp import web

from cco.integrator.mailbox import receive, send
from cco.integrator.message import no_message, quit
from cco.integrator.registry import getHandler, declare_handlers


async def start(ctx):
    port = ctx.config.get('port', 8123)
    app = web.Application()
    app['context'] = ctx
    routeCfgs = ctx.config.get('routes', [])
    app['routes'] = dict((r['name'], r) for r in routeCfgs)

    routes = [web.get(rc['path'], 
                      getHandler(ctx, rc['handler']),
                      name=rc['name']) 
                for rc in routeCfgs]
    app.add_routes(routes)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', port)
    await site.start()
    ctx.logger.info('%s finished' % ctx.pname)


def build_response(result, msg):
    data = {'result': result, 'message': msg}
    return web.json_response(data)

async def do_default(request):
    ctx = request.app['context']
    name = request.match_info.route.name
    cfg = request.app['routes'][name]
    #await send(ctx.parent_mb, Message())
    return build_response('ok', name)

async def do_poll(request):
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

async def do_quit(request):
    ctx = request.app['context']
    cfg = request.app['routes'][request.match_info.route.name]
    await send(ctx.parent_mb, quit)
    return build_response('ok', 'quit')


#*** register_handlers ***

def register_handlers(reg):
    declare_handlers(
            [start, do_default, do_poll, do_quit], 
            'server.web', reg)
