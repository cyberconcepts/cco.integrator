'''
A WSGI-compliant web server communicating with the top actor (dispatcher).

Server component: waitress
App based on: Werkzeug
  
2019-05-28 helmutm@cy55.de
'''

import json
from Queue import Empty
from waitress import serve
from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule

from cco.integrator.mailbox import receive, send
from cco.integrator.message import no_message, quit
from cco.integrator import registry


def start_waitress(ctx):
    port = ctx.config.get('port', 8123)
    app = create_app(ctx)
    serve(app, port=port, clear_untrusted_proxy_headers=True)


def create_app(ctx):

    url_map = Map([Rule('/quit', endpoint='quit'),
                   Rule('/poll', endpoint='poll')]) # TODO: create from conf
    handlers = dict(quit=do_quit, poll=do_poll) # TODO: create from conf

    def app(env, start_response):
        request = Request(env)
        urls = url_map.bind_to_environ(request.environ)
        resp = urls.dispatch(
            lambda ep, kw: handlers[ep](request, ctx, ep, **kw),
            catch_http_exceptions=False)
        return resp(env, start_response)

    return app


def build_response(result, msg):
    data = {'result': result, 'message': msg}
    return Response(json.dumps(data), mimetype='application/json')

def do_poll(request, ctx, ep, **kw):
    timeout = ctx.config.get('pollable_timeout', 15)
    msg = receive(ctx.parent_mb, timeout)
    if msg is no_message:
        data = ''
        result = 'idle'
    else:
        data = msg.payload # TODO: check message type
        result = 'data'
    return build_response(result, data)

def do_quit(request, ctx, ep, **kw):
    send(ctx.parent_mb, quit)
    return build_response('ok', 'quit')


def register_handlers(reg):
    registry.declare_handlers([start_waitress], 'webserver.wsgi', reg)
