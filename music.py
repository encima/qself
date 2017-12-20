import sys
import os
import datetime
import json
import csv
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

    def sort_last_fm(self):
        counts = []
        with open('data/lastfm.csv', 'r') as f:
            reader = csv.reader(f)
            scrobbles = list(reader)
            for s in scrobbles:
                found = False
                for c in counts:
                    if c[0] == s[0] and ((c[2].lower() in s[2].lower()) or (s[2].lower() in c[2].lower())):
                        c[4] += 1
                        found = True
                if not found:
                    s.append(1)
                    counts.append(s)
                # print(counts)
            sort_tracks = counts.sort(key = lambda x: x[4])
            # print(sort_tracks)
            with open('data/all_tracks.txt', 'w') as tracks:
                writer = csv.writer(tracks)
                writer.writerows(counts)
        print('done')
    
    def match_spotify(self, playlist, count=200, format='csv'):
        sorted_tracks = []
        with open('data/all_tracks.txt', 'r') as tracks:
            if format == 'json':
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
            elif format == 'csv':
                reader = csv.reader(tracks)
                all_tracks = list(reader)
                sorted_tracks = sorted(all_tracks, key=lambda k: int(k[4]), reverse=True)
        # fails without dumps because " are translated to '
        res = m.s.create_playlist('encima', json.dumps(playlist))
        pid = res.json()['id']
        uris = []
        index = 0
        matched = 0
        while matched < count:
            t = sorted_tracks[index]
            q = ''
            if format == 'csv':
                q = 'q=artist:{} track:{}&type=track'.format(t[0], t[2])
            elif format == 'json':
                q = 'q=artist:{} track:{}&type=track'.format(t['artist'], t['track'])
            res = m.s.search(q)
            if res.status_code == 200:
                results = res.json()['tracks']['items'] #maybe not the best assumption
                if (len(results) > 0):
                    track = results[0]
                    matched += 1
                    print(matched)
                    uris.append(track['uri'])
                    if(len(uris) == 100):
                        ids = ",".join(uris)
                        res = m.s.add_tracks_to_playlist('encima', pid, ids)
                        print(res)
                        uris.clear()
            index += 1
        

if __name__ == '__main__':
    m = Music()
    # m.s.auth.oauth_authorise()
    m.match_spotify({ "description": "Top 200 scrobbles from all years of all scrobbles", "public": "true", "name": "Top 200 2007-2017"}, 200, 'csv')
    # m.get_new_music()
    # m.sort_last_fm()
    
        