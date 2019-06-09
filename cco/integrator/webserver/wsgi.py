'''
A WSGI-compliant web server communicating with the top actor (dispatcher).

Server component: waitress
App based on: Werkzeug
  
2019-05-28 helmutm@cy55.de
'''

import json
from waitress import serve
from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule


def run_waitress(mailbox, receiver, logger, conf):
    port = conf.get('port', 8123)
    app = create_app(mailbox, receiver, conf)
    serve(app, port=port)


def create_app(mailbox, receiver, conf):

    url_map = Map([Rule('/quit', 'quit')]) # TODO: create from conf
    handlers = dict(quit=do_quit) # TODO: create from conf

    def app(env, start_response):
        request = Request(env)
        response = dispatch_request(request, mailbox, receiver, conf)
        urls = url_map.bind_to_envion(request.environ)
        return urls.dispatch(
            lambda ep, kw: handlers[ep](request, mailbox, receiver, conf, ep, **kw),
            catch_http_exceptions=True)

    return app


def build_response(result, msg):
    data = {'result': result, 'message': msg}
    return Response(json.dumps(data), mimetype='application/json')

def do_quit(request, mailbox, receiver, conf, ep, **kw):
    receiver.put('quit')
    return build_response('ok', 'quit')

