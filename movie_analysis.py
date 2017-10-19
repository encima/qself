import json
from datetime import datetime
import tmdbsimple as tmdb 
import requests
import collections
from collections import Counter
import config

checkins = None
today = datetime.today()
PAY_LOAD = {'api_key': config.tmdb['api_key']}
BASE_URL = "https://api.themoviedb.org/3/movie/{}"

def flatten(l):
	for el in l:
		if isinstance(el, collections.Iterable) and not isinstance(el, (str, bytes)):
			 yield from flatten(el)
		else:
			 yield el

def read_raw():
	with open('./data/checkins.json') as jsonfile:
		checkins = json.load(jsonfile)


	year_watched = []
	for c in checkins:
		c['watch_no'] = len(c['watched'])
		for w in c['watched']:
			if w is not None:
				w_date = datetime.fromtimestamp(int(w)/1000)
				if w_date.year == 2016 and c not in year_watched:
					year_watched.append(c)
				else:
					w = None
	print("You watched {0} movies".format(len(checkins)))
	rewatched = checkins
#[x for x in year_watched if x['watch_no'] > 1]

	rewatched = sorted(rewatched, key=lambda k: k['watch_no'], reverse=True)
	details = []
	genres = []
	for r in rewatched:
		if 'movie_id' in r:
			req = requests.get(BASE_URL.format(r['movie_id']), params = PAY_LOAD)
			res = req.json()
			res['watch_no'] = r['watch_no']
			details.append(res)
	with open('data/movie_checkins.json', 'w') as fp:
		json.dump(details, fp)

def read_formatted():
	with open('./data/movie_checkins.json') as jsonfile:
		checkins = json.load(jsonfile)
		genres = []
	print("You watched {0} movies".format(len(checkins)))
	for d in checkins:
		if 'genres' in d:
			 genre = [x['name'] for x in d['genres']]
			 genres.append(genre)
			 if d['watch_no'] > 1:
				 print("You watched {0} {1} times, which is a mix of {2}".format(d['title'], d['watch_no'], genre))
				 print('------')
	genres = flatten(genres)
	g_count = Counter(genres).most_common()
	for g in g_count:
		 print("{0} makes up {1}% of your watching".format(g[0], (g[1]/len(checkins))*100))

read_formatted()



