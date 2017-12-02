import requests
import configparser
from oauth import OauthHandler
import sqlite3

class SpotifyHandler:

    token = None

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.sp = self.config['spotify']
        self.base_url = self.sp['API_URL']
        self.auth = OauthHandler('spotify')
        self.access_token = self.auth.get_token()
        if not self.access_token:
            self.auth.oauth_authorise()


    def get_playlists(self, url = None):
        if not url:
            url = self.base_url + 'me/playlists'
        playlists_req = requests.get(url, headers={
                                'Authorization': "Bearer {}".format(self.access_token)})
        p = playlists_req.json()
        if 'error' in str(p) or playlists_req.status_code != 200:
            self.auth.oauth_authorise()
        playlists = (p['items'])
        return (playlists, p['next'])

    def get_tracks_from_playlist(self, owner, playlist, features=False):
        tracks_req = requests.get(self.base_url + 'users/{}/playlists/{}/tracks'.format(owner, playlist),
                headers={'Authorization': "Bearer {}".format(self.access_token)})
        t = tracks_req.json()
        if 'error' in t or tracks_req.status_code != 200:
            return 'error with access token'
        tracks = t['items']
        t_id = []
        for t in tracks:
            t_id.append(t['track']['id'])
        if features:
            self.get_track_features(t_id)
        return tracks

    def get_track_features(self, tracks):
        features_req = requests.get(self.base_url + 'audio-features?ids={}'.format(','.join(tracks)),
                headers={'Authorization': "Bearer {}".format(self.access_token)})
        f = features_req.json()
        if 'error' in f or features_req.status_code != 200:
            return 'error with access token'
        features = f['audio_features']
        for f in features:
            print(f)


