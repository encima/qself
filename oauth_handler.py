import json
import configparser
import requests

import oauth_server

class Oauth_Handler:

    def __init__(self, service):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini') 
        self.service = service

    def oauth_authorise(self, url):
        print("Go to the following URL and paste the code in the URL below:")
        print(url)
        s = oauth_server.start_server()

    def oauth_close(self):
        s = oauth_server.shutdown_server()

