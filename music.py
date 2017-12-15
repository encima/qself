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
            for x in p:
                if 'new music' in x['name'].lower():
                    playlists.append(x)
        else:
            print(len(playlists))
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
    # m.s.auth.oauth_authorise()
    # m.get_new_music()
    with open('data/new_tracks.txt', 'r') as tracks:
        all_tracks = json.load(tracks)
        formatted_tracks = {}
        for track in all_tracks:
            a = track['artist']
            t = track['title']
            k = '{}_{}'.format(a,t)
            if k in formatted_tracks:
                formatted_tracks[k]['count'] += track['count']
            else:
                formatted_tracks[k] = {'artist': a, 'count': track['count'], 'track': t}

        sorted_tracks = formatted_tracks.values()
        sorted_tracks = sorted(sorted_tracks, key=lambda k: k['count'], reverse=True)
        # fails without dumps because " are translated to '
        params = {
  "description": "Top 100 scrobbles from the past 5 years for my monthly playlists",
  "public": "true",
  "name": "New Music Top 100 2012-2017"
}
        # res = m.s.create_playlist('encima', json.dumps(params))
        uris = []
        index = 0
        matched = 0
        while matched < 100:
            t = sorted_tracks[index]
            q = 'q=artist:{} track:{}&type=track'.format(t['artist'], t['track'])
            res = m.s.search(q)
            if res.status_code == 200:
                results = res.json()['tracks']['items'] #maybe not the best assumption
                if (len(results) > 0):
                    track = results[0]
                    matched += 1
                    uris.append(track['uri'])
            index += 1
        ids = ",".join(uris)
        res = m.s.add_tracks_to_playlist('encima', '3YQYmTWGLN3ZIveuXm59p6', ids)
        print(res.status_code)