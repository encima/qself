import json
import configparser
import requests
import oauth_server as s
import sqlite3

class Oauth_Handler:

    def __init__(self, service):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini') 
        self.service = service
        self.auth = self.config[service]
        self.client_id = self.auth['CLIENT_ID']
        self.client_secret = self.auth['CLIENT_SECRET']
        self.redirect_uri = self.auth['REDIRECT']
        self.access_url = self.auth['TOKEN_URL']
        self.base_url = self.auth['API_URL']
        self.server = s.Oauth_Server()
        self.conn = sqlite3.connect('data/tokens.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS tokens (service text, token text)')
        self.conn.commit()

    def oauth_authorise(self):
        self.server.add_endpoint('/{}'.format(self.service), self.service, self.save_code)
        print("Go to the following URL and paste the code in the URL below:")
        print(self.build_url())
        self.server.serve()

    def build_url(self):
        auth = self.auth['AUTH_URL'] + self.config['oauth']['ARGS'].format(self.client_id, self.redirect_uri)
        return auth

    def get_token(self):
        self.cursor.execute('SELECT token FROM tokens WHERE service="{}"'.format(self.service))
        res = self.cursor.fetchone()
        if not res:
            self.oauth_authorise()
        else:
            return res[0]

    def oauth_close(self):
        self.server.shutdown()

    def oauth_token(self, url, args, method='GET'):
        if method == 'GET':
            r = requests.get(url, params=args)
        else:
            r = requests.post(url, data=args)
        return r.json()

    def save_code(self, args):
        print('CODE RECEIVED')
        self.oauth_close()
        params = {"client_id": self.client_id, "client_secret":self.client_secret,
                  "grant_type":"authorization_code", "redirect_uri":self.redirect_uri,
                  "code": args['code']}
        token_res = self.oauth_token(self.access_url, params, self.auth['TOKEN_VERB'])
        if 'access_token' in token_res:
            access_token = token_res['access_token']
            print(access_token)
            self.conn.cursor().execute('DELETE FROM tokens WHERE service="{}"'.format(self.service))
            self.conn.cursor().execute('INSERT INTO tokens VALUES(?,?)', (self.service, access_token))
            self.conn.commit()
            print('Saved new token')
            return access_token
        else:
            print('Something happened when trying to get your token')
            return None

