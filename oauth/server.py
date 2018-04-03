from flask import Flask, request, Response
from werkzeug.serving import make_server
from multiprocessing import Process
import threading
import os, sys
import configparser

class EndpointAction(object):

    def __init__(self, action):
        self.action = action
        self.response = Response(status=200, headers={})


    def __call__(self, *args):
        self.action(request.args)
        return self.response



class OauthServer(threading.Thread):

    def __init__(self,):
        threading.Thread.__init__(self)
        self.app = Flask('oauth')
        self.config = configparser.ConfigParser()
        self.config.read('config.ini') 
        settings = self.config['server']
        self.srv = make_server('127.0.0.1', settings['port'], self.app)
        self.ctx = self.app.app_context()
        self.ctx.push()
        self.add_endpoint('/shutdown', 'shutdown', self.shutdown_server, ['POST'])

    def run(self):
        print('starting server')
        self.srv.serve_forever()

    def shutdown(self):
        self.srv.shutdown()

    def shutdown_server(self, *args):
        func = request.environ.get('werkzeug.server.shutdown')
        print('server shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()

    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None, methods=['GET']):
        print('Adding endpoint for: ' + endpoint)
        self.app.add_url_rule(endpoint, endpoint_name, EndpointAction(handler), methods=methods)
