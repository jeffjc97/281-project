import csv, random
from utils import get_client

CLIENT = get_client()

def scrape_artist_list(file_name, limit=1000):
	found = 0
	popular = limit // 2
	artists = {}

	while found < limit:
		offset = found if found < popular else 50 * int(random.random() * 2000)
		response = CLIENT.search(
			"year:1990-2017", 
			type="artist", 
			limit=50,
			offset=offset
		)["artists"]["items"]
		for artist in response:
			artists[artist["id"]] = {
				"name": artist["name"],
				"popularity": artist["popularity"]
			}
		found = len(artists)
		print("Found {} artists so far!".format(found))
	
	print("Writing to CSV")
	with open(file_name, "w") as csvfile:
		headers = ["Artist ID", "Artist Name", "Popularity"]
		writer = csv.writer(csvfile)
		writer.writerow(headers)

		for artist_id, artist in artists.items():
			writer.writerow([artist_id, artist["name"], artist["popularity"]])