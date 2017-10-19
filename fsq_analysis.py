import json
import config
import requests


class FsqHandler:

    def __init__(self):
        self.client_id = config.foursquare['client_id']
        self.client_secret = config.foursquare['client_secret']
        self.redirect_uri = config.foursquare['redirect_uri']
        self.access_url = config.foursquare['access_url']
        self.access_token = config.foursquare['access_token']
        self.base_url = config.foursquare['base_url']
        if self.access_token == "":
            self.oauth_authorise()
        else:
            self.access_token = config.foursquare['access_token']

    def oauth_authorise(self):
        print("Go to the following URL and paste the code in the URL below:")
        auth = config.foursquare['auth_url'].format(self.client_id, self.redirect_uri)
        print(auth)
        key = input("Paste key here: ")
        print(key)
        params = {"client_id": self.client_id, "client_secret":self.client_secret,
                  "grant_type":"authorization_code", "redirect_uri":self.redirect_uri,
                  "code": key}
        auth_response = requests.get(self.access_url, params = params)
        j = auth_response.json()
        if 'error' not in j:
            self.access_token = j['access_token']
        else:
            print(j)

    def get_checkins(self):
        url = self.base_url + "users/self/checkins"
        checkins = []
        offset = 0
        total = 1000000 #set high and reduce since Python does not have a do while
        while offset < total:
            params = {"oauth_token":self.access_token, "afterTimestamp":1451606401,
                      "limit":250, "v":20161208, "offset":offset}
            res = requests.get(url, params = params)
            j = res.json()
            offset += 250
            total = j['response']['checkins']['count']
            print(offset)
            checkins.extend(j['response']['checkins']['items'])
        return checkins


if __name__ == '__main__':
    fsq = FsqHandler()
    checkins = fsq.get_checkins()
    with open('data/fsq_checkins.json', 'w') as fp:
        json.dump(checkins, fp)


#checkins = requests.post(config.foursquare["base_url"], data={'key':'value'})

