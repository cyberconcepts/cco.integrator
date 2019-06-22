'''
A simple webserver communicating with the top actor (dispatcher).
  
2019-05-28 helmutm@cy55.de
'''

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import json
from logging import getLogger
from Queue import Empty

from cco.integrator.mailbox import receive, send
from cco.integrator.message import no_message, quit


def run_server(ctx):
    port = ctx.config.get('port', 8000)
    httpd = HTTPServer(('localhost', port), Handler)
    httpd.active = True
    httpd.actorMailbox = ctx.mailbox
    httpd.parent_mb = ctx.parent_mb
    httpd.config = ctx.config
    # httpd.timeout = ...
    while httpd.active:
        httpd.handle_request()
        # httpd.active = check_mailbox(mailbox) != 'quit'


class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        routes = self.server.config.get('routes') or ['default']
        msg = self.path[1:]
        action = msg in routes and msg or 'default'
        route = getattr(self, 'route_' + action)
        route(msg)

    def route_default(self, msg):
        send(self.server.parent_mb, msg)
        self.respond(200, 'ok', msg)

    def route_quit(self, msg):
        msg = quit
        self.server.active = False
        self.route_default(msg)

    def route_poll(self, msg):
        timeout = self.server.config.get('pollable_timeout', 60)
        msg = receive(self.server.parent_mb, timeout)
        if msg is no_message:
            data = ''
            result = 'idle'
        else:
            data = msg.payload
            result = 'data'
        self.respond(200, result, data)

    def respond(self, rc, result, msg):
        self.send_response(rc)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        data = {'result': result, 'message': msg}
        self.wfile.write('%s\n' % json.dumps(data))

    def log_message(self, format, *args):
        logger = getLogger('integrator.webserver')
        logger.info(' - %s - %s' % (self.client_address[0], format % args))
