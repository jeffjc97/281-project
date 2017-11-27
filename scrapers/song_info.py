import csv
from utils import get_client

BATCH_SIZE = 50
CLIENT = get_client()

SIMPLE_HEADERS = [
	'song_id',
	'artist_id',
	'duration',
	'popularity',
	'artist_popularity',
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
	song_info = list(zip(
		CLIENT.tracks(tracks=batch_ids)['tracks'], 
		CLIENT.audio_features(tracks=batch_ids)
	))
	for song in song_info:
		data = {
			'song_id': song[0]['id'],
			'artist_id': song[0]['artists'][0]['id'],
			'duration': song[0]['duration_ms'],
			'explicit': int(song[0]['explicit']),
			'popularity': song[0]['popularity'],
			'danceability': song[1]['danceability'],
			'energy': song[1]['energy'],
			'key': song[1]['key'],
			'loudness': song[1]['loudness'],
			'mode': song[1]['mode'],
			'speechiness': song[1]['speechiness'],
			'acousticness': song[1]['acousticness'],
			'instrumentalness': song[1]['instrumentalness'],
			'liveness': song[1]['liveness'],
			'valence': song[1]['valence'],
			'tempo': song[1]['tempo'],
			'time_signature': song[1]['time_signature'],
		}
		data['artist_popularity'] = _get_popularity(song[0]['artists'][0]['id'])
		analytics = _get_analysis(song[0]['id'])
		data = {**data, **analytics}
		writer.writerow(_get_values(data))

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