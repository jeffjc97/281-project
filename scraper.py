import csv, datetime
from scrapers.artist_list import scrape_artist_list
from scrapers.spotify_charts import scrape_top_charts
from scrapers.artist_top_tracks import scrape_top_tracks
from scrapers.song_info import scrape_song_data

BEST_ARTISTS = "data/top_artists.csv"
BEST_SONGS = "data/top_songs.csv"
BEST_SONG_FEATURES = "data/top_song_features.csv"

RANDOM_ARTISTS = "data/random_artists.csv"
RANDOM_SONGS = "data/random_songs.csv"
RANDOM_SONG_FEATURES = "data/random_song_features.csv"

###########################################################################
### scrape data for top artists over the past year
###########################################################################

# top artists over the past year
scrape_top_charts(
	datetime.datetime(2016, 12, 30),
	datetime.datetime(2017, 11, 3),
	BEST_ARTISTS
)

# get top artists' songs
with open(BEST_ARTISTS, "r") as csvfile:
	reader = csv.reader(csvfile)
	artists = list(reader)[1:]
	artists = {
		artist[0]: artist[1] for artist in artists
	}
	scrape_top_tracks(artists, BEST_SONGS)

# get song data for all top songs
with open(BEST_SONGS, "r") as csvfile:
	reader = csv.reader(csvfile)
	songs = list(reader)[1:]
	song_ids = [song[2] for song in songs]
	scrape_song_data(song_ids[:1], BEST_SONG_FEATURES)

###########################################################################
### scrape data for random artists since 1990
###########################################################################

# get random artists
scrape_artist_list(RANDOM_ARTISTS, limit=100)

# get random artists' songs
with open(RANDOM_ARTISTS, "r") as csvfile:
	reader = csv.reader(csvfile); next(reader, None)
	artists = { row[0]: row[1] for row in reader }
	scrape_top_tracks(artists, RANDOM_SONGS)

# get song data for all random songs
with open(RANDOM_SONGS, "r") as csvfile:
	reader = csv.reader(csvfile); next(reader, None)
	song_ids = [ row[2] for row in reader ]
	scrape_song_data(song_ids, RANDOM_SONG_FEATURES)