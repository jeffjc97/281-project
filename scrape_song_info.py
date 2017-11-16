import csv
from utils import get_client

BATCH_SIZE = 50
CLIENT = get_client()

all_features = {}
with open('top_songs.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    songs = list(reader)[1:]
    N_BATCHES = int((len(songs) + BATCH_SIZE - 1) / BATCH_SIZE)
    
    song_ids = [song[2] for song in songs]
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
            # just get main artist?
            song_id = batch_ids[i]
            all_features[song_id] = {
                'song_id': song_id,
                'artist_id': song[0]['artists'][0]['id'],
                'artist_name': song[0]['artists'][0]['name'],
                'duration': song[0]['duration_ms'],
                'explicit': song[0]['explicit'],
                'song_name': song[0]['name'],
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
                'analysis_url': song[1]['analysis_url'],
            }

print("Writing to CSV")
with open('top_song_features.csv', 'w') as csvfile:
    headers = None
    writer = csv.writer(csvfile)
    for song in all_features:
        song_features = all_features[song]
        if not headers:
            headers = list(song_features.keys())
            writer.writerow(headers)
        writer.writerow(list(song_features.values()))
