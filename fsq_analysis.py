import json
import configparser
import requests
from Oauth import OauthHandler
import sqlite3
from datetime import datetime, timezone
import time, os

class FsqHandler:

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini') 
        self.fsq = self.config['foursquare']
        self.base_url = self.fsq['API_URL']
        self.auth = OauthHandler('foursquare')
        self.access_token = self.auth.get_token()
        os.environ['TZ']='UTC'
        if not self.access_token:
            self.auth.oauth_authorise()
    
    def get_checkins_for_range(self, start = None, end=None):
        url = self.base_url + "users/self/checkins"
        if not start:
            start = str(datetime.utcnow())
        d_format ='%Y-%m-%d %H:%M:%S'
        start = int(time.mktime(time.strptime(start,d_format)))
        checkins = []
        offset = 0
        total = 1000000 #set high and reduce since Python does not have a do while
        while offset < total:
            params = {"oauth_token":self.access_token, "afterTimestamp":start,
                      "limit":250, "v":20161208, "offset":offset}
            if end:
                params['beforeTimestamp'] = int(time.mktime(time.strptime(end, d_format)))
            res = requests.get(url, params = params)
            if res.status_code == 401:
                return False
            j = res.json()
            offset += 250
            if 'checkins' in j['response']:
                total = j['response']['checkins']['count']
                print(offset, total)
                checkins.extend(j['response']['checkins']['items'])
            else:
                break
        with open('data/fsq_checkins.json', 'w') as fp:
            json.dump(checkins, fp)
        return checkins


if __name__ == '__main__':
    fsq = FsqHandler()
    fsq.get_checkins_for_range('2015-7-27 00:00:00', '2017-7-27 23:59:00')

