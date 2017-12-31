import requests, json
from bs4 import BeautifulSoup as bs
import collections
import re
import logging

# decide album flow (either one album at a time or all at once)
#     so that means allowing for search of an album rather than just artist OR all albums together
# tokens
# web interface
# refactoring

spotify_url = 'https://api.spotify.com/v1/'
s_access_token = 'Bearer BQBAEWHtymP4CxDkVAVGRZZFYIUGszHS8b3Q868JJyAgc9g_FDbluHtxdhPbhftrlOMOQ43KFK6m7ANFcg4Q0rrk0aiVAxa4v5bMKoOwndHirSnzijOThkMLeDI-LhUW7pmQ2hnSU5X_xpE'
## search: returns artists or artist name
def spotify_search(query, search_type):
  url = spotify_url + "search"
  params = {
    'q': query,
    'type': search_type
  }
  sp_headers = {'Authorization': s_access_token}

  sp = requests.get(url, headers= sp_headers, params = params).json()
  check = sp.get('error')
  if check:
    print "Refresh Access Token"
  for artist in sp['artists']['items']:
      if artist['name'] == query:
          return artist['id'], artist['name']
  return sp['artists']['items']

def get_albums(artist_id):
  albums = []
  check = []
  sp_headers = {'Authorization': s_access_token}
  params = {
    'album_type': 'album'
  }
  url = spotify_url + "artists/" + artist_id + "/albums"
  sp = requests.get(url, headers= sp_headers, params = params).json()
  for album in sp['items']:
    if album['name'] in check:
        continue
    albums.append(album)
    check.append(album['name'])
  return albums

def request(url):
    sp_headers = {'Authorization': s_access_token}
    return requests.get(url, headers = sp_headers).json()

def get_song_titles(album):
  song_list = []
  url = spotify_url + "albums/" + album_id + "/tracks"
  response = request(url)
  for song in response['items']:
      if song['name'] not in song_list:
        song_list.append(song['name'])
        # [song['name']] = song['artists'][0]['name']
  return song_list


# get lyrics url
#
#
#

# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)
# requests_log = logging.getLogger("requests.packages.urllib3")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True

# pass lyrics url
def get_genius_lyrics_url(song_title, artist):
  # song_title = " ".join(song_title.split(" "))
  params = {'q': song_title}
  # sets up url
  g_headers = {'Authorization': 'Bearer YjmwPCJjvNtzHAEIwApGIBe-ASj29XurrSCu9qi1YyYfPtq-pPfoUPoLguUR7_l7'}
  g_url = "http://api.genius.com/search"
  gen = requests.get(g_url, params = params, headers = g_headers).json()
  song_info = None
  for hit in gen["response"]["hits"]:
    if hit["result"]["primary_artist"]["name"] == artist:
      song_info = hit
      break
  if song_info:
    return song_info
  print "No Genius Hits for Song"
  return None

def lyrics_from_song_url(song_url):
  page = requests.get(song_url)
  html = bs(page.text, "html.parser")
  lyrics = html.find('div', class_='lyrics').get_text()
  return lyrics.encode("utf-8")

def clean_lyrics(words):
  words = words.replace("\n", " ")
  words = words.replace(' {2,}', ' ')
  words = re.sub("[\(\[].*?[\)\]]", ' ', words)
  return words.lower().split(" ")

def count(words):
  stopwords = ['a', 'the', 'or', 'and', 'but', 'to', 'so', 'is', '', ' ']
  wordcount = {}
  for word in words:
    if word not in stopwords:
      if word not in wordcount:
        wordcount[word] = 1
      else:
        wordcount[word] += 1
  return wordcount

# gets all lyrics for each song and creates count
def album_lyrics(song_list, artist_name):
  lyrics_collection = collections.Counter()
  for song in song_list:
    g_song_info = get_genius_lyrics_url(song, artist_name)
    if not g_song_info:
      print "Error - No song found"
      continue
    lyrics = lyrics_from_song_url(g_song_info['result']['url'])
    lyrics_collection += create_counter(lyrics)
    print song
  return lyrics_collection

def create_counter(lyrics):
  word_dict = count(clean_lyrics(lyrics))
  return collections.Counter(word_dict)

# get an artist id and name from Spotify API
artist_id, artist_name = spotify_search('Kanye West', 'artist')
# returns album object for each artist from Spotify API
albums = get_albums(artist_id)

for album_obj in albums:
  print album_obj['name']

  # Gets Tracks from each Album from Spotify API
  song_list = get_song_titles(album_obj['id'])

  # Scrapes Genius API for each song and counts words used in each
  word_counter = album_lyrics(song_list, artist_name)
  if not word_counter:
      continue
  for word, repeats in word_counter.most_common(10):
    print(word, repeats)
