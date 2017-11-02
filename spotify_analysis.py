import requests
import configparser

class Spotify_Handler:
    
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini') 

    def get_playlists(self):
        playlists = requests.get(self.config['spotify']['url'] + '/v1/me/playlists', headers={
                                'Authorization': self.config['spotify']['token']})
        p = playlists.json()
        print(p)

    def oauth_authorise(self):
        print("Go to the following URL and paste the code in the URL below:")
        auth = "{}?client_id={}&scopes={}&response_type={}&redirect_uri={}".format(self.config['spotify']['auth_url'], self.config['spotify']['client_id'], self.config['spotify']['scopes'], 'code', 'http://localhost:8080') 
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
s.oauth_authorise()
# get_playlists()
