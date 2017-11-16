import json
import configparser
import requests
import oauth_handler as o
import sqlite3

class FsqHandler:

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini') 
        self.fsq = self.config['foursquare']
        self.client_id = self.fsq['CLIENT_ID']
        self.client_secret = self.fsq['CLIENT_SECRET']
        self.redirect_uri = self.fsq['REDIRECT']
        self.access_url = self.fsq['TOKEN_URL']
        self.base_url = self.fsq['API_URL']
        self.o = o.Oauth_Handler('foursquare')
        self.conn = sqlite3.connect('data/tokens.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS tokens (service text, token text)')
        self.conn.commit()
        self.cursor.execute('SELECT token FROM tokens WHERE service="foursquare"')
        res = self.cursor.fetchone()
        if not res:
            self.oauth_authorise()
        else:
            self.access_token = res[0]
            if not self.get_checkins():
                self.oauth_authorise()
                self.get_checkins()

    def oauth_authorise(self):
        self.o.server.add_endpoint('/foursquare', 'Foursquare', self.save_code)
        url = self.build_url()
        self.o.oauth_authorise(url)

    def build_url(self):
        auth = self.fsq['AUTH_URL'] + self.config['oauth']['ARGS'].format(self.client_id, self.redirect_uri)
        return auth


    def save_code(self, args):
        print('CODE RECEIVED')
        self.o.oauth_close()
        params = {"client_id": self.client_id, "client_secret":self.client_secret,
                  "grant_type":"authorization_code", "redirect_uri":self.redirect_uri,
                  "code": args['code']}
        token_res = self.o.oauth_token(self.access_url, params, 'GET')
        if 'access_token' in token_res:
            self.access_token = token_res['access_token']
            self.conn.cursor().execute('DELETE FROM tokens WHERE service="foursquare"')
            self.conn.cursor().execute('INSERT INTO tokens VALUES(?,?)', ('foursquare', self.access_token))
            self.conn.commit()
            print('Saved new token')
        else:
            print('Something happened when trying to get your token')


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
                return false
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
    checkins = fsq.get_checkins()

