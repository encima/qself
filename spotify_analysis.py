import requests
import configparser
import oauth_handler as o
import sqlite3

class Spotify_Handler:

    token = None

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.sp = self.config['spotify']
        self.client_id = self.sp['CLIENT_ID']
        self.client_secret = self.sp['CLIENT_SECRET']
        self.redirect_uri = self.sp['REDIRECT']
        self.access_token = ""
        self.base_url = self.sp['API_URL']
        self.conn = sqlite3.connect('tokens.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS tokens (service text, token text)')
        self.conn.commit()
        self.cursor.execute('SELECT token FROM tokens WHERE service="spotify"')
        self.access_token = self.cursor.fetchone()[0]
        if not self.access_token:
            self.oauth_authorise()
        else: 
            print(self.access_token[0])
            self.get_playlists()


    def get_playlists(self):
        playlists = requests.get(self.base_url + 'me/playlists', headers={
                                'Authorization': "Bearer {}".format(self.access_token)})
        p = playlists.json()
        print(p)

    def build_url(self):
        auth = self.sp['AUTH_URL'] + self.config['oauth']['ARGS'].format(self.client_id, self.redirect_uri)
        return auth

    def oauth_authorise(self):
        self.o = o.Oauth_Handler('spotify')
        self.o.server.add_endpoint('/spotify', 'Spotify', self.save_code)
        url = self.build_url()
        self.o.oauth_authorise(url)

    def save_code(self, args):
        self.token = args['code']
        self.o.oauth_close()
        token_res = self.o.oauth_token(self.sp['TOKEN_URL'], {'redirect_uri':self.sp['REDIRECT'], 'code':self.token, 'grant_type':"authorization_code", 'client_id':self.config['spotify']['CLIENT_ID'], 'client_secret':self.sp['CLIENT_SECRET']}, 'POST')
        self.access_token = token_res['access_token']
        self.conn.cursor().execute('INSERT INTO tokens VALUES(?,?)', ('spotify', self.access_token))
        self.conn.commit()
        self.refresh_token = token_res['refresh_token']


s = Spotify_Handler()
