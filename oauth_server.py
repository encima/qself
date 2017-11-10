from flask import Flask, render_template,request, Response
from multiprocessing import Process
import os, sys

class EndpointAction(object):

    def __init__(self, action):
        self.action = action
        self.response = Response(status=200, headers={})


    def __call__(self, *args):
        self.action(request.args)
        return self.response


class Oauth_Server(object):
    app = None
    p = None

    def __init__(self, name='oauth'):
        self.app = Flask(name)

    def serve(self):
        args_dict = {'port':8080}
        self.app.run(port=8080)
        self.p = Process(target=self.app.run, kwargs=args_dict)
        self.p.start()

    def shutdown(self):
        #self.p.terminate()
        pass

    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None):
        print('Adding endpoint for: ' + endpoint)
        self.app.add_url_rule(endpoint, endpoint_name, EndpointAction(handler))



