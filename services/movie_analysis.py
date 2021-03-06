import json
from datetime import datetime
import tmdbsimple as tmdb
import requests
import collections
from collections import Counter
import configparser
import urllib.parse



class MovieHandler:

    def __init__(self):
        self.checkins = None
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        today = datetime.today()
        self.PAY_LOAD = {'api_key': self.config['tmdb']['api_key']}
        self.BASE_URL = "https://api.themoviedb.org/3/movie/{}"        
        self.read_checkins()

    def flatten(self, l):
        for el in l:
            if isinstance(
                    el, collections.Iterable) and not isinstance(el, (str, bytes)):
                yield from self.flatten(el)
            else:
                yield el

    def read_checkins(self):
        with open('./data/movie_checkins.json') as jsonfile:
            self.checkins = json.load(jsonfile)

    def get_movies_on_date(self, start, end=None):
        matching = []
        if not end:
            end = start
        for c in self.checkins:
            if len(c['watched']) > 0:
                for w_date in c['watched']:
                    if w_date is not None:
                        w = datetime.fromtimestamp(int(w_date / 1000))
                        if w >= start and w <= end:
                            # date.day == w.day and date.month == w.month and w.year == date.year:
                            matching.append(c)
        return matching

    def read_raw(self):
        year_watched = []
        for c in self.checkins:
            c['watch_no'] = len(c['watched'])
            for w in c['watched']:
                if w is not None:
                    w_date = datetime.fromtimestamp(int(w) / 1000)
                    if w_date.year == 2016 and c not in year_watched:
                        year_watched.append(c)
                    else:
                        w = None
        print("You watched {0} movies".format(len(self.checkins)))
        rewatched =self.checkins.copy()
        #[x for x in year_watched if x['watch_no'] > 1]

        rewatched = sorted(rewatched, key=lambda k: k['watch_no'], reverse=True)
        details = []
        genres = []
        for r in rewatched:
            if 'movie_id' in r:
                req = requests.get(self.BASE_URL.format(r['movie_id']), params=self.PAY_LOAD)
                res = req.json()
                res['watch_no'] = r['watch_no']
                details.append(res)
        with open('data/movie_checkins.json', 'w') as fp:
            json.dump(details, fp)


    def read_formatted(self, movies):
        if not movies:
            movies = self.checkins
        genres = []
        print("You watched {0} movies".format(len(movies)))
        for d in movies:
            if 'movie_id' in d:
                title = urllib.parse.quote_plus(d['movie_id'])
                movie = requests.get(self.BASE_URL.format(title), params=self.PAY_LOAD)
                details = movie.json()
                if 'genres' in details:
                    genre = [x['name'] for x in details['genres']]
                    genres.append(genre)
                    print("You watched {0} {1} times, which is a mix of {2}".
                        format(d['movie'], len(d['watched']), genre))
                    print('------')
        genres = self.flatten(genres)
        g_count = Counter(genres).most_common()
        for g in g_count:
            print("{0} makes up {1}% of your watching".format(
                g[0], (g[1] / len(movies)) * 100))

if __name__ == '__main__':
    m = MovieHandler()
    s = datetime.strptime('2017-04-01', '%Y-%m-%d')
    e = datetime.strptime('2017-05-07', '%Y-%m-%d')
    watched = m.get_movies_on_date(s, e)
    print(watched) 
