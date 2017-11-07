import json
import configparser
import requests
import oauth_server as s

class Oauth_Handler:

    def __init__(self, service):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini') 
        self.service = service
        self.server = s.Oauth_Server()

    def oauth_authorise(self, url):
        print("Go to the following URL and paste the code in the URL below:")
        print(url)
        self.server.serve()

    def oauth_close(self):
        self.server.shutdown()

    def oauth_token(self, url, args):
        r = requests.post(url, data=args)
        return r.json()

