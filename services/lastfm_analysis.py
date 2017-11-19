import pylast
from datetime import datetime, timezone
import configparser

class LastfmHandler:

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini') 
        self.last = self.config['lastfm']
        self.network = pylast.LastFMNetwork(api_key=self.last['CLIENT_ID'], api_secret=self.last['CLIENT_SECRET'], username=self.last['USERNAME'], password_hash=self.last['HASH'])
        
    def get_tracks_for_range(self, start, end):
        start = start.replace(tzinfo=timezone.utc).timestamp()
        end = end.replace(tzinfo=timezone.utc).timestamp()
        tracks = self.network.get_user('encima').get_recent_tracks(limit=200, time_from=start, time_to=end)
        print(tracks)


if __name__== '__main__':
    l = LastfmHandler()
    start = datetime(2017, 7, 27, 00, 1)
    end = datetime(2017, 7, 27, 23, 59)
    l.get_tracks_for_range(start, end)