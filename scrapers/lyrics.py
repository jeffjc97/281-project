import datetime
import csv
import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool

base_url = "http://api.genius.com"
search_url = base_url + "/search"
headers = {'Authorization': 'Bearer 9iwI3VG-MaxZWQ2aC03jE6cNe9Lyl3zpfDhCsuteA2hATgUVhCUjg6A12SjScEUZ'}


def lyrics_from_song_url(page_url):
    content = requests.get(page_url).content.decode('ascii', 'ignore')
    html = BeautifulSoup(content, "html.parser")
    # cleanup
    [h.extract() for h in html('script')]
    [tag.replaceWith(tag.text) for tag in html.find_all('a')]
    [tag.replaceWith(tag.text) for tag in html.find_all('br')]
    # at least Genius is nice and has a tag called 'lyrics'!
    lyrics = html.find("div", {"class": "lyrics"})
    if lyrics:
        return lyrics.text
    return ""

def get_lyrics(song):
    print("Finding lyrics for " + song[1] + " by " + song[0])
    params = {'q': song[0] + " " + song[1]}
    response = requests.get(search_url, params=params, headers=headers)
    hits = response.json()['response']['hits']
    if len(hits):
        found_song = False
        for hit in hits:
            if not found_song:
                # assuming that this is the correct song (will have to check after)
                if hit['type'] == 'song':
                    song_api_url = base_url + hit['result']['api_path']
                    params = {'q': song[1]}
                    response = requests.get(song_api_url, params=params, headers=headers)
                    song_url = response.json()['response']['song']['url']
                    lyrics = lyrics_from_song_url(song_url)
                    unformatted_lyrics = lyrics.replace('\n', ' ').replace('\r', '').lower()
                    song[3] = unformatted_lyrics
                    found_song = True
                    return song
    else:
        # print("Error finding " + song[1] + " by " + song[0])
        return None

def scrape_lyrics():
    csvfile = open('data/random_song_lyrics.csv', 'w')
    writer = csv.writer(csvfile)
    writer.writerow(["Artist", "Title", "ID", "Lyrics"])

    hdrs = None
    data = None

    # with open('data/random_songs.csv', 'r', encoding='latin-1') as f:
    with open('data/top_songs.csv') as f:
        reader = csv.reader(f)
        all_rows = list(reader)
        data = all_rows[1:]

    # song artist, song name, song spotify ID, lyrics
    songs = [[d[1], d[3], d[2], None] for d in data]

    for song in songs:
        get_lyrics(song)

    with Pool(processes=8) as pool:
        for song_data in pool.map(get_lyrics, songs, 1):
            if song_data is None:
                continue
            writer.writerow(song_data)

scrape_lyrics()
