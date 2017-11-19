import sys
import os
import datetime
from services import *

sys.path.insert(0, os.path.abspath('..'))

from clint.arguments import Args 
from clint.textui import puts, colored, indent, prompt, validators

d_format ='%Y-%m-%d %H:%M:%S'

args = Args()

m = MovieHandler()
s = SpotifyHandler()
l = LastfmHandler()
f = FsqHandler()

for arg in args.all:
    if arg == 'day':
        date = datetime.datetime.today()
        if len(args) == 2:
            day = args[1]
            date = datetime.datetime.strptime(day, '%Y-%m-%d')
        print('On {}'.format(date)) 
        movies = m.get_movies_on_date(date)
        start_date = date.replace(hour=0, minute=0)
        end_date = date.replace(hour=23, minute=59)
        places = f.get_checkins_for_range(datetime.datetime.strftime(start_date, d_format), datetime.datetime.strftime(end_date, d_format), d_format, False)
        tracks = l.get_tracks_for_range(start_date, end_date)
        prompt.puts('You watched {} movies that day'.format(len(movies)))
        prompt.puts('You went to {} places that day'.format(len(places)))
        prompt.puts('You listened to {} tracks that day'.format(len(tracks)))
    elif arg =='recommend':
        choice = 'movie'
        if len(args) == 2:
            choice = args[2]
