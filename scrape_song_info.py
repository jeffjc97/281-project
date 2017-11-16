import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import csv
import urllib
import ssl
import datetime

client_id = 'f08e082307684817bf52a1651e9f004a'
client_secret = 'cb7f448bc5524573ace26ade5a92c561'
client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

gcontext = ssl.SSLContext()
batch_size = 50

all_features = {}

with open('top_songs.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        songs = list(reader)[1:]
        song_ids = [song[2] for song in songs]
        for batch in range(int(len(songs) / batch_size) + 1):
            print("Spotify API: batch", batch, "of", int(len(songs) / batch_size))
            batch_ids = song_ids[batch_size * batch: batch_size * (batch + 1)]
            song_info = list(zip(sp.tracks(tracks=batch_ids)['tracks'], sp.audio_features(tracks=batch_ids)))
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
