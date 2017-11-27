import csv, datetime
from utils import get_client

BATCH_SIZE = 50
CLIENT = get_client()

SIMPLE_HEADERS = [
	'song_id',
	'artist_id',
	'duration',
	'popularity',
	'explicit',
	'danceability',
	'energy',
	'loudness',
	'speechiness',
	'acousticness',
	'instrumentalness',
	'liveness',
	'valence',
	'tempo',
	'time_signature',
	'mode',
	'key',
	'track_number',
	'artist_popularity',
	'album_length',
	'release_date',
]
ANALYSIS_HEADERS = [
	'end_of_fade_in',
	'start_of_fade_out',
	'tempo_confidence',
	'time_signature_confidence',
	'mode_confidence',
	'key_confidence',
	'num_bars',
	'num_beats',
	'num_tatums',
	'num_sections',
	'num_segments',
]
HEADERS = SIMPLE_HEADERS + ANALYSIS_HEADERS
def _get_values(dict):
	return list(map(lambda h: dict[h], HEADERS))

albums = {}
def _get_album(album_id):
	if album_id in albums:
		return albums[album_id]
	album = CLIENT.album(album_id)
	date = album['release_date'].split("-")
	year, month, day = int(date[0]) - 1990, int(date[1]), int(date[2])
	albums[album_id] = {
		'album_length': len(album['tracks']['items']),
		'release_date': year * 365 + month * 30 + day
	}
	return albums[album_id]

artist_popularities = {}
def _get_popularity(artist_id):
	if artist_id in artist_popularities:
		return artist_popularities[artist_id]
	popularity = CLIENT.artist(artist_id)['popularity']
	artist_popularities[artist_id] = popularity
	return popularity

def _get_analysis(analysis_url):
	analysis = CLIENT.audio_analysis(analysis_url)
	return {
		'end_of_fade_in': 				analysis['track']['end_of_fade_in'],
		'start_of_fade_out': 			analysis['track']['start_of_fade_out'],
		'tempo_confidence': 			analysis['track']['tempo_confidence'],
		'time_signature_confidence': 	analysis['track']['time_signature_confidence'],
		'mode_confidence': 				analysis['track']['mode_confidence'],
		'key_confidence': 				analysis['track']['key_confidence'],
		'num_bars': 					len(analysis['bars']),
		'num_beats': 					len(analysis['beats']),
		'num_tatums': 					len(analysis['tatums']),
		'num_sections': 				len(analysis['sections']),
		'num_segments': 				len(analysis['segments']),
	}

def _handle(batch_ids, writer):
	# get a new SSL connection once in a while
	CLIENT = get_client()
	song_info = list(zip(
		CLIENT.tracks(tracks=batch_ids)['tracks'], 
		CLIENT.audio_features(tracks=batch_ids)
	))

	written = 0
	for song in song_info:
		data = {
			'song_id': song[0]['id'],
			'artist_id': song[0]['artists'][0]['id'],
			'duration': song[0]['duration_ms'],
			'popularity': song[0]['popularity'],
			'explicit': int(song[0]['explicit']),
			'danceability': song[1]['danceability'],
			'energy': song[1]['energy'],
			'loudness': song[1]['loudness'],
			'speechiness': song[1]['speechiness'],
			'acousticness': song[1]['acousticness'],
			'instrumentalness': song[1]['instrumentalness'],
			'liveness': song[1]['liveness'],
			'valence': song[1]['valence'],
			'tempo': song[1]['tempo'],
			'time_signature': song[1]['time_signature'],
			'mode': song[1]['mode'],
			'key': song[1]['key'],
			'track_number': song[0]['track_number'],
		}
		data['artist_popularity'] = _get_popularity(song[0]['artists'][0]['id'])
		
		album_data = _get_album(song[0]['album']['id'])
		analytics = _get_analysis(song[0]['id'])
		data = {**data, **album_data, **analytics}
		
		writer.writerow(_get_values(data))
		print("Wrote data for song {}/{}: {}".format(
			written + 1,
			len(song_info), 
			song[0]['name']
		))
		written += 1

def scrape_song_data(song_ids, file_name):
	N_BATCHES = int((len(song_ids) + BATCH_SIZE - 1) / BATCH_SIZE)
	batches = [
		song_ids[BATCH_SIZE * i:BATCH_SIZE * (i + 1)]
		for i in range(N_BATCHES)
	]
	
	csvfile = open(file_name, "w")
	writer = csv.writer(csvfile)
	writer.writerow(HEADERS)
	
	for batch_index, batch_ids in enumerate(batches):
		print("Working on batch {:02d} of {:02d}".format(
			batch_index + 1, N_BATCHES
		))
		_handle(batch_ids, writer)