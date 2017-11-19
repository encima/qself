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
        self.t = TastekidHandler()
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
                
                movies_table = [['Movies: {}'.format(len(movies))]]
                for x in movies:
                    movies_table.append([x['movie']])
                table = AsciiTable(movies_table)
                print(table.table)
                
                places_table = [['Places: {}'.format(len(places))]]
                for x in places:
                    places_table.append([x['venue']['name']])
                table = AsciiTable(places_table)
                print(table.table)

                music_table = [['Music: {}'.format(len(tracks))]]
                for x in tracks:
                    music_table.append([x.track])
                table = AsciiTable(music_table)
                print(table.table)
            elif arg =='recommend':
                choice = 'movie'
                if len(args) >= 2:
                    choice = args[1]
                choice = choice.lower()
                print('Recommending {}'.format(choice))
                if choice == 'movies' or choice == 'books':
                    q = [(args[2], args[3])]
                    recs = self.t.get_similar(q, choice)
                    movies_table = [['{}: {}'.format(choice.title(), len(recs))]]
                    for x in recs:
                        movies_table.append([x['Name'], x['wUrl']])
                    table = AsciiTable(movies_table)
                    print(table.table)
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
            elif arg == 'summary':
                movies = self.m.checkins
                print('{} movies'.format(len(movies)))
                checkins = self.f.get_checkins_for_range()
                print('{} places'.format(len(checkins)))
                tracks = self.l.get_all_tracks()
                print('{} tracks'.format(tracks))

if __name__ == '__main__':
    q = Qself()
    args = Args()
    q.prompt(args)