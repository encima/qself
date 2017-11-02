import json
import configparser
import requests

class Oauth_Handler:

    def __init__(self, service):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini') 

    def oauth_authorise(self, service, url):
        print("Go to the following URL and paste the code in the URL below:")
        print(url)
        pass

    def oauth_access(self):
        pass

    