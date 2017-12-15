import sys
import os
import datetime
import json
import csv
from services import *
from geopy.geocoders import Nominatim
from terminaltables import AsciiTable

scrobbles = []
spot_tracks = []

with open('data/lastfm.csv', 'r') as f:
  reader = csv.reader(f)
  scrobbles = list(reader)

# with open('data/lastfm.csv', 'r') as lfm:
#     reader = csv.reader(lfm)
#     scrobbles = list(reader)

with open('data/tracks.txt', 'r') as spot:
    spot_tracks = json.load(spot)

print(len(scrobbles))
print(len(spot_tracks))

def find_track(title, artist):
  count = 0
  for scrobble in scrobbles:
    if artist.lower() == scrobble[0].lower() and title.lower() == scrobble[2].lower():
      count += 1
  return count

totals = []
for track in spot_tracks:
  track['count'] = find_track(track['title'], track['artist'])
spot_tracks = sorted(spot_tracks, key=lambda k: k['count'], reverse=True)
with open('data/new_tracks.txt', 'w') as tracks:
  json.dump(spot_tracks, tracks)
top_hundred = spot_tracks[0:99]
with open('data/new_tracks_hundred.txt', 'w') as tracks:
  json.dump(top_hundred, tracks)
