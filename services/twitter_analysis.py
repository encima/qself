import requests
import configparser
from oauth import OauthHandler
import sqlite3

class TwitterHandler:

    token = None

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.auth = OauthHandler('twitter')
        self.access_token = self.auth.get_token()
        if not self.access_token:
            self.auth.oauth_authorise()