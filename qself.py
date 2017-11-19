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


class Qself:

    def __init__(self):
        self.m = MovieHandler()
        self.s = SpotifyHandler()
        self.l = LastfmHandler()
        self.f = FsqHandler()
        self.geolocator = Nominatim()

    def prompt(self, args):
        for arg in args.all:
            if arg == 'day':
                date = datetime.datetime.today()
                if len(args) == 2:
                    day = args[1]
                    date = datetime.datetime.strptime(day, '%Y-%m-%d')
                print('On {}'.format(date)) 
                movies = self.m.get_movies_on_date(date)
                start_date = date.replace(hour=0, minute=0)
                end_date = date.replace(hour=23, minute=59)
                places = self.f.get_checkins_for_range(datetime.datetime.strftime(start_date, d_format), datetime.datetime.strftime(end_date, d_format), d_format, False)
                tracks = self.l.get_tracks_for_range(start_date, end_date)
                prompt.puts('You watched {} movies that day'.format(len(movies)))
                movies_table = [x['movie'] for x in movies]
                table = AsciiTable(movies_table)
                print(table.table)
                prompt.puts('You went to {} places that day'.format(len(places)))
                prompt.puts('You listened to {} tracks that day'.format(len(tracks)))
            elif arg =='recommend':
                choice = 'movie'
                if len(args) >= 2:
                    choice = args[1]
                choice = choice.lower()
                print('Recommending {}'.format(choice))
                if choice == 'movie':
                    pass
                elif choice == 'places':
                    location = self.geolocator.geocode(args[2])
                    print('Your lat and long is {} {}'.format(location.latitude, location.longitude))
                    places = self.f.get_recommended_places_nearby(location.latitude, location.longitude, args[3], args[4])
                    places_table = [['Place', 'Distance(m)', 'Why?']]
                    for r in places:
                        for i in r['items']:
                            places_table.append([i['venue']['name'], i['venue']['location']['distance'], i['reasons']['items'][0]['summary']])
                    table = AsciiTable(places_table)
                    print(table.table)

if __name__ == '__main__':
    q = Qself()
    args = Args()
    q.prompt(args)