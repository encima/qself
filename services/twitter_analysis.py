import requests
import configparser
from oauth import OauthHandler
import sqlite3
import random
import urllib
import time
import base64, hmac
from hashlib import sha1

class TwitterHandler:

    token = None

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.tw = self.config['twitter']
        self.auth = OauthHandler('twitter')
        self.access_token = self.auth.get_token()
        if not self.access_token:
            self.get_request_token()
            # self.auth.oauth_authorise()

    def add_auth_header(self, url, method, token=None):
        # https://dev.twitter.com/web/sign-in/implementing
        cb = 'oauth_callback="{}"'.format(self.tw['REDIRECT'])
        key = 'oauth_consumer_key="{}"'.format(self.tw['CLIENT_ID'])
        n = ''.join([str(random.randint(0, 9)) for i in range(32)])
        nonce = 'oauth_nonce="{}"'.format(n)
        sig_method = 'oauth_signature_method="HMAC-SHA1"'
        signing_key = urllib.parse.quote(self.tw['CLIENT_SECRET'], '') + '&'
        if token:
            signing_key += urllib.parse.quote(self.tw['CLIENT_SECRET'], '')
        timestamp = 'oauth_timestamp="{}"'.format(int(time.time()))
        oauth_version = 'oauth_version="1.0"'
        params = "{}&{}&{}&{}&{}&{}".format(cb, key, nonce, sig_method, timestamp, oauth_version)
        # https://developer.twitter.com/en/docs/basics/authentication/guides/creating-a-signature.html
        base_string = "{}&{}&{}".format(method, urllib.parse.quote(url), urllib.parse.quote(params))
        print(base_string)
        signature = urllib.parse.quote(base64.standard_b64encode(hmac.new(signing_key.encode(), base_string.encode(), sha1).digest()).decode('ascii'))
        header_string = 'OAuth {}, {}, {}, oauth_signature="{}", {}, {}, {}'.format(cb, key, nonce, signature, sig_method, timestamp, oauth_version)
        print(header_string)
        return (params, {'Authorization': header_string})

    def get_request_token(self):
        u = self.tw['REQUEST_URL']
        p, h = self.add_auth_header(u, 'GET')
        r = requests.get(u, headers=h)
        print(r.request.headers)
        print(r.request.url)
        print(r.json())