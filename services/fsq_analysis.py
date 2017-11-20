import json
import configparser
import requests
from oauth import OauthHandler
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

    def get_recommended_places_nearby(self, lat, lng, type='query', term=None):
        url = self.base_url + "venues/explore"
        ll = '{},{}'.format(lat, lng)
        params = {'oauth_token': self.access_token, 'll':ll, "v":20161208, 'sortByDistance': 1}
        if term:
            params[type] = term
        res = requests.get(url, params=params)
        j = res.json()
        return j['response']['groups']

    def get_total_checkins(self):
        url = self.base_url + "users/self/checkins"
        params = {"oauth_token":self.access_token, "v":"20161208"}
        res = requests.get(url, params = params)
        if res.status_code == 401:
            return False
        j = res.json()
        if 'checkins' in j['response']:
            return j['response']['checkins']['count']
        else:
            return False

    def get_checkins_for_range(self, start = None, end=None, d_format ='%Y-%m-%d %H:%M:%S', paging = True):
        url = self.base_url + "users/self/checkins"
        if not start:
            start = datetime.strftime(datetime.utcnow(), d_format)
        int_start = int(time.mktime(time.strptime(start, d_format)))
        int_end = None
        if end:
            int_end = int(time.mktime(time.strptime(end, d_format)))
        checkins = []
        offset = 0
        limit = 250 if paging else 100
        total = 1000000  if paging else limit #set high and reduce since Python does not have a do while
        while offset < total:
            params = {"oauth_token":self.access_token, "afterTimestamp":int_start,
                      "limit":limit, "v":20161208, "offset":offset}
            if int_end:
               params['beforeTimestamp'] = int_end
            res = requests.get(url, params = params)
            if res.status_code == 401:
                return False
            j = res.json()
            offset += limit
            if 'checkins' in j['response']:
                total = j['response']['checkins']['count'] if paging else total
                checkins.extend(j['response']['checkins']['items'])
            else:
                break
        with open('data/fsq_checkins.json', 'w') as fp:
            json.dump(checkins, fp)
        return checkins


if __name__ == '__main__':
    fsq = FsqHandler()
    fsq.get_checkins_for_range('2015-7-27 00:00:00', '2017-7-27 23:59:00')

