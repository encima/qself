import json
import configparser
import requests
from Oauth import OauthHandler
import sqlite3

class FsqHandler:

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini') 
        self.fsq = self.config['foursquare']
        self.base_url = self.fsq['API_URL']
        self.auth = OauthHandler('foursquare')
        self.access_token = self.auth.get_token()
        if not self.access_token or not self.get_checkins():
            self.auth.oauth_authorise()
        else:
            self.get_checkins()
    
    def get_checkins(self):
        url = self.base_url + "users/self/checkins"
        checkins = []
        offset = 0
        total = 1000000 #set high and reduce since Python does not have a do while
        while offset < total:
            params = {"oauth_token":self.access_token, "afterTimestamp":1451606401,
                      "limit":250, "v":20161208, "offset":offset}
            res = requests.get(url, params = params)
            if res.status_code != 200:
                return False
            j = res.json()
            offset += 250
            total = j['response']['checkins']['count']
            print(offset)
            checkins.extend(j['response']['checkins']['items'])
        with open('data/fsq_checkins.json', 'w') as fp:
            json.dump(checkins, fp)
        return checkins


if __name__ == '__main__':
    fsq = FsqHandler()

