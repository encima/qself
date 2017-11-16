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
        self.conn = sqlite3.connect('data/tokens.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS tokens (service text, token text)')
        self.conn.commit()
        self.cursor.execute('SELECT token FROM tokens WHERE service="spotify"')
        res = self.cursor.fetchone()
        if not res:
            self.oauth_authorise()
        else:
            self.access_token = res[0]
            if not self.get_playlists():
                self.oauth_authorise()
            self.get_playlists()


    def get_playlists(self):
        playlists_req = requests.get(self.base_url + 'me/playlists', headers={
                                'Authorization': "Bearer {}".format(self.access_token)})
        p = playlists_req.json()
        if 'error' in p or playlists_req.status_code != 200:
            return False
        playlists = p['items']
        for p in playlists:
            self.get_tracks_from_playlist(p['owner']['id'], p['id'])
        return True

    def get_tracks_from_playlist(self, owner, playlist):
        tracks_req = requests.get(self.base_url + 'users/{}/playlists/{}/tracks'.format(owner, playlist),
                headers={'Authorization': "Bearer {}".format(self.access_token)})
        t = tracks_req.json()
        tracks = t['items']
        t_id = []
        for t in tracks:
            t_id.append(t['track']['id'])
        self.get_track_features(t_id)

    def get_track_features(self, tracks):
        features_req = requests.get(self.base_url + '/v1/audio-features?ids={}'.format(','.join(tracks)),
                headers={'Authorization': "Bearer {}".format(self.access_token)})
        print(features_req.text)
        f = features_req.json()
        features = f['audio_features']
        for f in features:
            print(f)

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
        self.conn.cursor().execute('DELETE FROM tokens WHERE service="spotify"')
        self.conn.cursor().execute('INSERT INTO tokens VALUES(?,?)', ('spotify', self.access_token))
        self.conn.commit()
        print('Saved new token')
        self.refresh_token = token_res['refresh_token']


s = Spotify_Handler()
