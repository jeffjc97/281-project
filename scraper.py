import csv, datetime
from utils import str_date, get_weeks, ssl_request

from scrapers.artist_songs import scrape_artists
from scrapers.spotify_charts import scrape_charts
from scrapers.song_info import scrape_songs

scrape_charts(
	datetime.datetime(2016, 12, 30), 
	datetime.datetime(2017, 11, 3),
	"data/top_songs.csv"
)

with open('data/top_songs.csv', 'r') as csvfile:
	reader = csv.reader(csvfile)
	songs = list(reader)[1:]
	song_ids = [song[2] for song in songs]
	scrape_songs(song_ids, "data/song_features.csv")

with open("data/song_features.csv", "r") as csvfile:
	reader = csv.reader(csvfile)
	songs = list(reader)[1:]
	artists = {
		song[1]: song[2] for song in songs
	}
	scrape_artists(artists, "data/artist_songs.csv")

# with open("data/artist_songs.csv"), "r") as csvfile:
# 	reader = csv.reader(csvfile)
