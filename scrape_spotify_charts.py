import csv
import urllib.request
import ssl
import datetime

gcontext = ssl.SSLContext()

start_date = datetime.datetime(2017, 11, 3)
end_date = datetime.datetime(2016, 12, 30)
week = datetime.timedelta(weeks=1)
song_data = {}

cur = start_date
while cur >= end_date:
    interval_end = cur.strftime('%Y-%m-%d')
    interval_start = (cur - week).strftime('%Y-%m-%d')
    print("Reading top songs for", interval_end)
    url = 'http://spotifycharts.com/regional/global/weekly/' + interval_start + '--' + interval_end + '/download'
    response = urllib.request.urlopen(url,  context=gcontext)
    cr = csv.reader(response.read().decode('utf-8').splitlines())
    next(cr, None)
    for row in cr:
        # gets one messed up row, oops
        if len(row) == 5 and row[4].rsplit('/', 1)[-1] not in song_data:
            song_data[row[4].rsplit('/', 1)[-1]] = [row[1], row[2]]
    cur -= week

print("Writing to CSV")
with open('top_songs.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Artist", "Title", "Spotify URL"])
        for song in song_data:
            writer.writerow([song_data[song][1], song_data[song][0], song])
