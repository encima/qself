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