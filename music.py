import sys
import os
import datetime
import json
from services import *
from geopy.geocoders import Nominatim
from terminaltables import AsciiTable

sys.path.insert(0, os.path.abspath('..'))

from clint.arguments import Args
from clint.textui import puts, colored, indent, prompt, validators

d_format = '%Y-%m-%d %H:%M:%S'


class Music:

    def __init__(self):
        self.s = SpotifyHandler()
        self.l = LastfmHandler()

    def get_new_music(self):
        all_tracks = []
        playlists, next = self.s.get_playlists()
        while next:
            p, next = self.s.get_playlists(next)
            playlists.append(p)
        else:
            for pl in playlists:
                print(pl)
                if 'name' in pl:
                    name = pl['name']
                    if 'new music' in name.lower():
                        tracks = self.s.get_tracks_from_playlist(
                            'encima', pl['id'])
                        for t in tracks:
                            track = {}
                            track['artist'] = t['track']['artists'][0]['name']
                            track['title'] = t['track']['name']
                            track['playlist'] = name
                            try:
                                track = self.l.get_track(track)
                                all_tracks.append(track)
                            except BaseException:
                                print('{} Not found'.format(track['title']))
            with open('data/tracks.txt', 'w') as tracks:
                json.dump(all_tracks, tracks)


if __name__ == '__main__':
    m = Music()
    # m.get_new_music()
    with open('data/tracks.txt', 'r') as tracks:
        t = json.load(tracks)
        newlist = sorted(t, key=lambda k: k['count'])
