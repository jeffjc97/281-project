import csv
from utils import get_client

CLIENT = get_client()

# artists should be a dictionary from ids to names
def scrape_top_tracks(artists, file_name):
	artist_ids = set(artists.keys())
	print("Retrieving songs for {} unique artists...".format(len(artists)))

	with open(file_name, "w+") as song_file:
		writer = csv.writer(song_file)
		writer.writerow([
			"Artist ID",
			"Artist Name",
			"Song ID",
			"Song Title"
		])
		for artist_index, artist_id in enumerate(artist_ids):
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