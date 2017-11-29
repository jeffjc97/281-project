import csv, datetime, json, requests, time
import spotipy
from utils import get_client
from multiprocessing import Pool

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
def _get_album(client, album_id):
	if album_id in albums:
		return albums[album_id]
	album = client.album(album_id)
	date = album['release_date'].split("-")
	year, month, day = int(date[0]) - 1990, 0 if len(date) < 2 else int(date[1]), 0 if len(date) < 3 else int(date[2])
	albums[album_id] = {
		'album_length': len(album['tracks']['items']),
		'release_date': year * 365 + month * 30 + day
	}
	return albums[album_id]

artist_popularities = {}
def _get_popularity(client, artist_id):
	if artist_id in artist_popularities:
		return artist_popularities[artist_id]
	popularity = client.artist(artist_id)['popularity']
	artist_popularities[artist_id] = popularity
	return popularity

def _get_analysis(client, analysis_url):
	analysis = client.audio_analysis(analysis_url)
	if analysis is None:
		return None
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

def handle_song(song):
	if song is None or song[0] is None or song[1] is None:
		return None
	client = get_client()
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
	try:
		data['artist_popularity'] = _get_popularity(client, song[0]['artists'][0]['id'])
		album_data = _get_album(client, song[0]['album']['id'])
		analytics = _get_analysis(client, song[0]['id'])
		if analytics is None:
			return None
		data = {**data, **album_data, **analytics}
		print("Got data for song {}".format(song[0]['name']))
		return data
	except requests.exceptions.SSLError:
		print("SSL Error!")
		return None
	except requests.exceptions.ConnectionError:
		print("Connection Error!")
		return None
	except spotipy.oauth2.SpotifyOauthError:
		print("OAuth Error!")
		return None
	except json.decoder.JSONDecodeError:
		print("JSON Error!")
		return None
	except requests.exceptions.HTTPError:
		print("URL Not Found!")
		return None
	except spotipy.client.SpotifyException:
		print("Analysis Not Found!")
		return None

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
		song_info = list(zip(
			CLIENT.tracks(tracks=batch_ids)['tracks'], 
			CLIENT.audio_features(tracks=batch_ids)
		))	
		start_time = time.time()
		with Pool(processes=8) as pool:
			for song_data in pool.map(handle_song, song_info, 1):
				if song_data is None:
					continue
				writer.writerow(_get_values(song_data))
		batch_time = time.time() - start_time
		print("Batch total time: {:.2f}".format(batch_time))