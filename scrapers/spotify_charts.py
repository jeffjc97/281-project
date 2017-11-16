import csv, datetime
from utils import str_date, get_weeks, ssl_request

GLOBAL_WEEKLY_URL = 'http://spotifycharts.com/regional/global/weekly/{}--{}/download'

def scrape_charts(start, end, file_name):
	weeks = get_weeks(start, end)
	print("Retrieving global song data for {} weeks...".format(len(weeks)))

	song_data = {}
	for week in weeks:
		(start, end) = week
		response = ssl_request(GLOBAL_WEEKLY_URL.format(start, end))

		cr = csv.reader(response.read().decode('utf-8').splitlines())
		next(cr, None)
		for row in cr:
			# gets one messed up row, oops
			if len(row) == 5 and row[4].rsplit('/', 1)[-1] not in song_data:
				song_data[row[4].rsplit('/', 1)[-1]] = [row[1], row[2]]
		print("Finished with {} to {}".format(start, end))

	print("Writing to CSV")
	with open(file_name, 'w') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(["Artist", "Title", "Spotify ID"])
		for song in song_data:
			writer.writerow([song_data[song][1], song_data[song][0], song])