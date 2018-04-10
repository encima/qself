import json
import configparser
import requests
from oauth.server import OauthServer
import sqlite3

class OauthHandler:

    def __init__(self, service):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini') 
        self.service = service
        self.auth = self.config[service]
        self.client_id = self.auth['CLIENT_ID']
        self.client_secret = self.auth['CLIENT_SECRET']
        self.redirect_uri = self.auth['REDIRECT']
        self.access_url = self.auth['TOKEN_URL']
        self.token_key = self.auth['TOKEN_KEY'] or 'access_token'
        self.base_url = self.auth['API_URL']
        self.server = None
        self.conn = sqlite3.connect('data/tokens.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS tokens (service text, token text)')
        self.conn.commit()

    def oauth_authorise(self, url = None, cb = None):
        if not self.server:
            self.server = OauthServer()
        if not cb:
            cb = self.save_code
        self.server.add_endpoint('/{}'.format(self.service), self.service, cb)
        print("Go to the following URL and paste the code in the URL below:")
        if not url:
            url = self.build_url()
        print(url)
        self.server.start()
        # requests.post('http://localhost:8080/shutdown')

    def build_url(self):
        auth = self.auth['AUTH_URL']
        if self.config[self.service]['ARGS']:
            auth += self.config[self.service]['ARGS']
        else:
            auth = self.auth['AUTH_URL'] + self.config['oauth']['ARGS'].format(self.client_id, self.redirect_uri)
        return auth

    def get_token(self):
        self.cursor.execute('SELECT token FROM tokens WHERE service="{}"'.format(self.service))
        res = self.cursor.fetchone()
        if not res:
            return None
        else:
            return res[0] 

    def convert_token(self):
        pass

    def oauth_close(self):
        self.server.shutdown_server(None)
        # requests.post('http://localhost:8080/shutdown')
        self.server = None

    def oauth_token(self, url, args, method = 'GET', header = None):
        if method == 'GET':
            r = requests.get(url, params=args, headers=header)
        else:
            r = requests.post(url, data=args, headers=header)
        return r

    def sign_request(self, key, base_string):
        from hashlib import sha1
        import hmac

        hashed = hmac.new(key.encode(), base_string.encode(), sha1)

        # The signature
        return hashed.digest().encode("base64").rstrip('\n')

    def save_code(self, args):
        print('CODE RECEIVED')
        params = {"client_id": self.client_id, "client_secret":self.client_secret,
                  "grant_type":"authorization_code", "redirect_uri":self.redirect_uri,
                  "code": args['code']}
        token_res = self.oauth_token(self.access_url, params, self.auth['TOKEN_VERB']).json()
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

