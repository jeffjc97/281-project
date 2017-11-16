import csv
from utils import get_client

BATCH_SIZE = 50
CLIENT = get_client()

songs = None
with open('top_song_features.csv', 'r') as csvfile:
	reader = csv.reader(csvfile)
	songs = list(reader)[1:]

N_BATCHES = int((len(songs) + BATCH_SIZE - 1) / BATCH_SIZE)
artists = {
	song[1]: song[2] for song in songs
}
artist_ids = set(artists.keys())
print("Found {} unique artists!".format(len(artists)))

with open("artist_songs.csv", "w+") as song_file:
	writer = csv.writer(song_file)
	writer.writerow([
		"Artist ID",
		"Artist Name",
		"Song ID",
		"Song Title",
		"Popularity"
	])
	for artist_index, artist_id in enumerate(artist_ids):
		# if (artist_index + 1 % 10) == 0:
		print("Working on artist number {}".format(artist_index + 1))
		urn = 'spotify:artist:' + artist_id
		track_data = CLIENT.artist_top_tracks(urn)
		if track_data is None:
			print("Didn't find data for artist {}".format(artists[artist_id]))
			continue
		for track in track_data['tracks']:
			writer.writerow([
				artist_id,
				artists[artist_id],
				track['id'],
				track['name']
			])