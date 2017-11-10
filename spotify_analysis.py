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
        url = s.build_url()
        self.o.oauth_authorise(url)

    def save_code(self, args):
        self.token = args['code']
        self.o.oauth_close()
        token_res = self.o.oauth_token(self.sp['TOKEN_URL'], {'redirect_uri':self.sp['REDIRECT'], 'code':self.token, 'grant_type':"authorization_code", 'client_id':self.config['spotify']['CLIENT_ID'], 'client_secret':self.sp['CLIENT_SECRET']}, 'POST')
        self.access_token = token_res['access_token']
        self.refresh_token = token_res['refresh_token']


s = Spotify_Handler()
s.oauth_authorise()
# s.get_playlists()
