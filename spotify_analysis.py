import requests
import configparser
import oauth_handler as o
import sqlite3

class Spotify_Handler:

    token = None

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

    def get_playlists(self):
        playlists = requests.get(self.config['spotify']['API_URL'] + 'me/playlists', headers={
                                'Authorization': self.access_token})
        p = playlists.json()
        print(p)

    def build_url(self):
        auth = "{}?client_id={}&scopes={}&response_type={}&redirect_uri={}".format(self.config['spotify']['AUTH_URL'], self.config['spotify']['CLIENT_ID'], self.config['spotify']['SCOPES'], 'code', self.config['spotify']['REDIRECT'])
        return auth

    def request(self):
        self.o = o.Oauth_Handler('spotify')
        self.o.server.add_endpoint('/spotify', 'Spotify', s.save_code)
        url = s.build_url()
        self.o.oauth_authorise(url)

    def save_code(self, args):
        print(args['code'])
        self.token = args['code']
        self.o.oauth_close()
        access_token = self.o.oauth_token(self.config['spotify']['TOKEN_URL'], {'redirect_uri':self.config['spotify']['REDIRECT'], 'code':self.token, 'grant_type':"authorization_code", 'client_id':self.config['spotify']['CLIENT_ID'], 'client_secret':self.config['spotify']['CLIENT_SECRET']})
        print(access_token)
        self.access_token = access_token['access_token']


s = Spotify_Handler()
s.request()
s.get_playlists()
