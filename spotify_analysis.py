import requests
import configparser
import oauth_handler as o

class Spotify_Handler:
    
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

    def get_playlists(self):
        playlists = requests.get(self.config['spotify']['url'] + '/v1/me/playlists', headers={
                                'Authorization': self.config['spotify']['token']})
        p = playlists.json()
        print(p)

    def build_url(self):
        auth = "{}?client_id={}&scopes={}&response_type={}&redirect_uri={}".format(self.config['spotify']['AUTH_URL'], self.config['spotify']['CLIENT_ID'], self.config['spotify']['SCOPES'], 'code', self.config['spotify']['REDIRECT'])
        return auth

    def oauth_authorise(self):
        print("Go to the following URL and paste the code in the URL below:")
        print(auth)
        key = input("Paste key here: ")
        print(key)
        # j = auth_response.json()
        # if 'error' not in j:
        #     pass
        #     # self.access_token = j['access_token']
        # else:
        #     print(j)

s = Spotify_Handler()
o = o.Oauth_Handler('spotify')
url = s.build_url()
o.oauth_authorise(url)
code = input('Code here:')
o.oauth_close()
# get_playlists()
