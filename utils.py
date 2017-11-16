import datetime, ssl
import urllib.request
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

CLIENT_ID = 'f08e082307684817bf52a1651e9f004a'
CLIENT_SECRET = 'cb7f448bc5524573ace26ade5a92c561'

def str_date(date):
    return date.strftime('%Y-%m-%d')

def get_weeks(start, end):
    dates = [start]
    week = datetime.timedelta(weeks=1)
    while dates[-1] < end:
        dates.append(dates[-1] + week)
    dates = list(map(str_date, dates))
    weeks = list(map(
        lambda i: (dates[i], dates[i + 1]), 
        range(len(dates) - 1)
    ))
    return weeks

def ssl_request(url):
    return urllib.request.urlopen(url, context=ssl.SSLContext())

def get_client():
	creds = SpotifyClientCredentials(CLIENT_ID, CLIENT_SECRET)
	return spotipy.Spotify(client_credentials_manager=creds)