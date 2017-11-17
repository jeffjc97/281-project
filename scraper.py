import csv, datetime
from utils import str_date, get_weeks, ssl_request

from scrapers.artist_list import scrape_artist_list
from scrapers.artist_top_tracks import scrape_top_tracks
from scrapers.spotify_charts import scrape_top_charts
from scrapers.song_info import scrape_song_data

TOP_CHARTS_SONGS = "data/top_songs.csv"
TOP_CHARTS_SONG_FEATURES = "data/top_song_features.csv"
TOP_CHARTS_ARTIST_SONGS = "data/top_artist_songs.csv"
TOP_CHARTS_ARTIST_SONG_FEATURES = "data/top_artist_song_features.csv"

ARTIST_LIST_5000 = "data/5000_artist_list.csv"
ARTIST_LIST_5000_SONGS = "data/5000_artist_songs.csv"
ARTIST_LIST_5000_SONG_FEATURES = "data/5000_artist_song_features.csv"

# scrape_top_charts(
# 	datetime.datetime(2016, 12, 30), 
# 	datetime.datetime(2017, 11, 3),
# 	TOP_CHARTS_SONGS
# )

# with open(TOP_CHARTS_SONGS, 'r') as csvfile:
# 	reader = csv.reader(csvfile)
# 	songs = list(reader)[1:]
# 	song_ids = [song[2] for song in songs]
# 	scrape_song_data(song_ids, TOP_CHARTS_SONG_FEATURES)

# with open(TOP_CHARTS_SONGS_FEATURES, "r") as csvfile:
# 	reader = csv.reader(csvfile)
# 	songs = list(reader)[1:]
# 	artists = {
# 		song[1]: song[2] for song in songs
# 	}
# 	scrape_top_tracks(artists, TOP_CHARTS_ARTIST_SONGS)

# with open(TOP_CHARTS_ARTIST_SONGS, "r") as csvfile:
# 	reader = csv.reader(csvfile)
# 	songs = list(reader)[1:]
# 	song_ids = [song[2] for song in songs]
# 	scrape_song_data(song_ids, TOP_CHARTS_ARTIST_SONG_FEATURES)

# scrape_artist_list(ARTIST_LIST_5000, limit=5000)

# with open(ARTIST_LIST_5000, "r") as csvfile:
# 	reader = csv.reader(csvfile); next(reader, None)
# 	artists = { row[0]: row[1] for row in reader }
# 	scrape_top_tracks(artists, ARTIST_LIST_5000_SONGS)

# with open(ARTIST_LIST_5000_SONGS, "r") as csvfile:
# 	reader = csv.reader(csvfile); next(reader, None)
# 	song_ids = [ row[2] for row in reader ]
# 	scrape_song_data(song_ids, ARTIST_LIST_5000_SONG_FEATURES)