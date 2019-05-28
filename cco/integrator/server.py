'''
A simple webserver communicating with the top actor (dispatcher).
  
2019-04-23 helmutm@cy55.de

'''

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import json
from logging import getLogger
from Queue import Queue, Empty
from threading import Thread


def run_server(mailbox, receiver, logger, conf):
    port = conf.get('port', 8000)
    httpd = HTTPServer(('localhost', port), Handler)
    httpd.active = True
    httpd.actorMailbox = mailbox
    httpd.parent_mb = receiver
    httpd.config = conf
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
        self.server.parent_mb.put(msg)
        self.respond(200, 'ok', msg)

    def route_quit(self, msg):
        self.server.active = False
        self.route_default(msg)

    def route_poll(self, msg):
        timeout = self.server.config.get('pollable_timeout', 60)
        try:
            data = self.server.parent_mb.get(timeout=timeout)
            result = 'data'
        except Empty:
            data = ''
            result = 'idle'
        self.respond(200, result, data)

    def respond(self, rc, result, msg):
        self.send_response(rc)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        data = {'result': result, 'message': msg}
        self.wfile.write('%s\n' % json.dumps(data))

    def log_message(self, format, *args):
        logger = getLogger('service.server')
        logger.info(' - %s - %s' % (self.client_address[0], format % args))
