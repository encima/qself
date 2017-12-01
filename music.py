import sys
import os
import datetime
from services import *
from geopy.geocoders import Nominatim
from terminaltables import AsciiTable

sys.path.insert(0, os.path.abspath('..'))

from clint.arguments import Args 
from clint.textui import puts, colored, indent, prompt, validators

d_format ='%Y-%m-%d %H:%M:%S'

class Music:

  def __init__(self):
        self.s = SpotifyHandler()
        self.l = LastfmHandler()

if __name__ == '__main__':
    m = Music()
    p = m.s.get_playlists()
    for pl in p:
        name = pl['name']
        if 'new music' in name.lower():
            print(pl)
            print('-----')
            tracks = m.s.get_tracks_from_playlist('encima', pl['id'])
            print(len(tracks))


