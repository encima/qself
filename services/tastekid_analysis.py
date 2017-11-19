import requests
# from imdb_api import IMDBApi as ia
import json
import configparser

class TastekidHandler:

  def __init__(self):
    self.config = configparser.ConfigParser()
    self.config.read('config.ini') 
    self.tk = self.config['tastekid']
    self.base_url = self.tk['API_URL']
    self.client_id = self.tk['client_id']
    self.client_secret = self.tk['client_secret']

  def get_similar(self, terms, returnType):
    res = self.api_call(terms, returnType)
    if 'Similar' in res:
      return res['Similar']['Results']
    else:
      print(res)
      return None

  # make call to tastekid
  def api_call(self, params, returnType='movies'):
    paramString = ''
    for p in params:
      paramString += '{}:{},'.format(p[0], p[1])
    #authenticate
    params = {
      'q': paramString,
      'type': returnType,
      'k': self.client_secret,
      'info': 1
    }
    response = requests.get(self.base_url, params=params)
    return response.json()

if __name__ == '__main__':
  t = TastekidHandler()
  resp = t.get_similar([('music','Keaton Henson'), ('music', 'Hans Zimmer')], 'music')
  print(resp)