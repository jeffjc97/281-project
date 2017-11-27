import csv, datetime, re
from utils import str_date, get_weeks, ssl_request, get_client

song_id_re = re.compile('^[0-9a-zA-Z]{22}$')

BATCH_SIZE = 50
CLIENT = get_client()
GLOBAL_WEEKLY_URL = 'http://spotifycharts.com/regional/global/weekly/{}--{}/download'

def scrape_top_charts(start, end, file_name):
	weeks = get_weeks(start, end)
	print("Retrieving global top artists for {} weeks...".format(len(weeks)))

	song_data = {}
	for week in weeks:
		(start, end) = week
		response = ssl_request(GLOBAL_WEEKLY_URL.format(start, end))

		cr = csv.reader(response.read().decode('utf-8').splitlines())
		next(cr, None)
		for row in cr:
			# gets one messed up row, oops
			if len(row) != 5:
				continue
			song_id = row[4].rsplit('/', 1)[-1]
			if song_id in song_data or song_id_re.match(song_id) is None:
				continue
			song_data[song_id] = [row[1], row[2]]
		print("Finished with {} to {}".format(start, end))

	song_ids = list(set(song_data.keys()))
	artist_ids = {}
	print("Found {} songs total; retrieving artists now...".format(len(song_ids)))

	N_BATCHES = int((len(song_ids) + BATCH_SIZE - 1) / BATCH_SIZE)
	batches = [
		song_ids[BATCH_SIZE * i:BATCH_SIZE * (i + 1)]
		for i in range(N_BATCHES)
	]

	for batch_index, batch_ids in enumerate(batches):
		print("Working on batch {:02d} of {:02d}".format(
			batch_index + 1, N_BATCHES
		))
		song_info = list(zip(
			CLIENT.tracks(tracks=batch_ids)['tracks'], 
			CLIENT.audio_features(tracks=batch_ids)
		))
		for i, song in enumerate(song_info):
			artist_ids[song[0]['artists'][0]['id']] = song[0]['artists'][0]['name']
	
	print("Found {} unique artists! Writing to CSV now".format(len(artist_ids)))
	with open(file_name, "w") as csvfile:
		headers = ['Artist ID', 'Artist Name']
		writer = csv.writer(csvfile)
		writer.writerow(headers)
		for artist_id, artist_name in artist_ids.items():
			writer.writerow([artist_id, artist_name])
