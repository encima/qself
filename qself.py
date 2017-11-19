import sys
import os
import datetime
from services import *

sys.path.insert(0, os.path.abspath('..'))

from clint.arguments import Args 
from clint.textui import puts, colored, indent

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
        print(date) 
        movies = m.get_movies_on_date(date)
        print(movies)
    elif arg =='recommend':
        choice = 'movie'
        if len(args) == 2:
            choice = args[2]
