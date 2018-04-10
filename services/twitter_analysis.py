import requests
import configparser
from oauth import OauthHandler
import sqlite3
import random
import urllib
import time
import json
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
            self.app_auth()
        else:
            results = self.search_tweets('Trump')
            tweets = []
            for t in results['statuses']:
                tweets.append({'text': t['text'], 'user': t['user']['screen_name'], 'date': t['created_at']})
            f = open('data/twitter_tasks.json', 'w')
            f.write(json.dumps(tweets))
            f.close()

    def app_auth(self):
        key_secret = '{}:{}'.format(self.tw['CLIENT_ID'], self.tw['CLIENT_SECRET']).encode('ascii')
        b64_encoded_key = base64.b64encode(key_secret)
        b64_encoded_key = b64_encoded_key.decode('ascii')
        headers = {
            'Authorization': 'Basic {}'.format(b64_encoded_key),
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
        }        
        auth_data = {
            'grant_type': 'client_credentials'
        }
        auth =requests.post('https://api.twitter.com/oauth2/token', headers=headers, data=auth_data)
        token = auth.json()['access_token']
        if auth.status_code == 200:
            self.auth.conn.cursor().execute('DELETE FROM tokens WHERE service="{}"'.format(self.auth.service))
            self.auth.conn.cursor().execute('INSERT INTO tokens VALUES(?,?)', (self.auth.service, token))
            self.auth.conn.commit()
        else:
            print('Error getting token')
            

    def build_auth_header(self, url, method = 'POST', token = None):
        NONCE = ""
        for i in range(32):
            NONCE += chr(random.randint(97, 122))
        params = {}
        if token:
            params = {
                'oauth_consumer_key': self.tw['CLIENT_ID'],
                'oauth_nonce': NONCE,
                'oauth_signature_method': 'HMAC-SHA1',
                'oauth_timestamp': str(int(time.time())),
                'oauth_token': token,
                'oauth_version': "1.0"
            }
        else:
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
        print(BASE_STRING)
        print('----')
        print(SIGNING_KEY)
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
        header = self.build_auth_header(url = self.tw['TOKEN_URL'], token=args['oauth_token'])
        token_res = self.auth.oauth_token(self.tw['TOKEN_URL'], params, self.tw['TOKEN_VERB'], header).text
        token_res = dict(urllib.parse.parse_qsl(token_res))
        if self.auth.token_key in token_res:
            access_token = token_res[self.auth.token_key]
            self.auth.conn.cursor().execute('DELETE FROM tokens WHERE service="{}"'.format(self.auth.service))
            self.auth.conn.cursor().execute('INSERT INTO tokens VALUES(?,?)', (self.auth.service, json.dumps(token_res)))
            self.auth.conn.commit()
            print('Saved new token')
            self.auth.oauth_close()
            return access_token 
        else:
            print('Something happened when trying to get your token')
            self.auth.oauth_close()
            return None

    def search_tweets(self, term):
        url = self.tw['API_URL'] + 'search/tweets.json'
        print(self.access_token)
        h = {'Authorization': 'Bearer {}'.format(self.access_token)}
        p = {'q': term, }
        r = requests.get(url, params = p, headers = h)
        if r.status_code == 200:
            return r.json()
