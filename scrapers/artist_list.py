import csv
from utils import get_client

CLIENT = get_client()

def scrape_artist_list(file_name, limit=1000):
	found = 0
	artists = {}
	while found < limit:
		response = CLIENT.search(
			"year:1990-2017",
			type="artist",
			limit=50,
			offset=found
		)["artists"]["items"]
		for artist in response:
			artists[artist["id"]] = artist["name"]
		found = len(artists)
	
	print("Writing to CSV")
	with open(file_name, "w") as csvfile:
		headers = ["Artist ID", "Artist Name"]
		writer = csv.writer(csvfile)
		writer.writerow(headers)

		for artist_id, artist in artists.items():
			writer.writerow([artist_id, artist])