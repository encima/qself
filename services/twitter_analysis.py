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
            resp = self.get_request_token().split('&')
            token = resp[0].split('=')[1]
            url =self.tw['AUTH_URL'] + self.tw['ARGS'].format(token=token)
            print(url)
            self.auth.oauth_authorise(url, self.save_code)
            

    def build_auth_header(self, url, method = 'POST', token = None):
        NONCE = ""
        for i in range(32):
            NONCE += chr(random.randint(97, 122))
        params = {
            'oauth_callback': self.tw['REDIRECT'],
            'oauth_consumer_key': self.tw['CLIENT_ID'],
            'oauth_nonce': NONCE,
            'oauth_signature_method': 'HMAC-SHA1',
            'oauth_timestamp': str(int(time.time())),
            'oauth_version': "1.0"
        }

        HEADER_TITLE = "Authorization"

        #Timestamp
        TIMESTAMP = str(int(time.time()))

        #Signature
        PARAMETER_STRING = '&'.join('{}={}'.format(key,val) for (key,val) in params.items())
        BASE_STRING = method + '&' + urllib.parse.quote(url, '') + '&' + urllib.parse.quote(PARAMETER_STRING, '')
        SIGNING_KEY = urllib.parse.quote(self.tw['CLIENT_SECRET'], '') + '&'
        if token:
            SIGNING_KEY += urllib.parse.quote(token, '')
            params['oauth_token'] = token
        params['oauth_signature'] = urllib.parse.quote(base64.standard_b64encode(hmac.new(SIGNING_KEY.encode(), BASE_STRING.encode(), sha1).digest()).decode('ascii'))

        HEADER = "OAuth "
        HEADER += ', '.join('{}={}'.format(key,val) for (key,val) in params.items())
        print(HEADER)
        return {HEADER_TITLE: HEADER}

    def get_request_token(self):
        u = self.tw['REQUEST_URL']
        h = self.build_auth_header(u, 'GET')
        r = requests.get(u, headers=h)
        return r.text
    
    def save_code(self, args):
        print('CODE RECEIVED')
        params = {"oauth_verifier": args['oauth_verifier']}
        print(args)
        header = self.build_auth_header(url = self.tw['TOKEN_URL'], token=args['oauth_token'])
        token_res = self.auth.oauth_token(self.tw['TOKEN_URL'], params, self.auth['TOKEN_VERB'] or 'POST', header)
        if self.token_key in token_res:
            access_token = token_res['access_token']
            print(access_token)
            self.conn.cursor().execute('DELETE FROM tokens WHERE service="{}"'.format(self.service))
            self.conn.cursor().execute('INSERT INTO tokens VALUES(?,?)', (self.service, access_token))
            self.conn.commit()
            print('Saved new token')
            self.oauth_close()
            return access_token 
        else:
            print('Something happened when trying to get your token')
            self.oauth_close()
            return None