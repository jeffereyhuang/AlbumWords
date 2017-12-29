import requests, json

# if comma, support multiple keywords
spotify_track_id = "7hNx9Dynz2fRO41L9AEVA8"

# sets up url
sp_params = {

}

sp_headers = {'Authorization': 'Bearer BQAqLsju_P2fU1yNPIC37iyvq6HmyIo_3cQ10ySBRUCXRSId6SZhsDchX9r0v9fBIsbDGXJ5RpTScS9tRV65Hp4j43wpZKmgyFivYurJEWslGvzg1SIgyoF7JAsBesBLBIQ-oZtN4LeK9P0'}

spotify_url = 'https://api.spotify.com/v1/tracks/' + spotify_track_id
sp = requests.get(spotify_url, headers= sp_headers, params = sp_params).json()

# response
# data = json.loads(spot)
song = sp['name']
artist = sp['artists'][0]['name']

print song, artist


genius_artist_id = "72"
# sets up url
g_params = {

}
g_headers = {'Authorization': 'Bearer YjmwPCJjvNtzHAEIwApGIBe-ASj29XurrSCu9qi1YyYfPtq-pPfoUPoLguUR7_l7'}
g_url = "http://api.genius.com/artists/" + genius_artist_id + "/songs"
gen = requests.get(g_url, headers = g_headers, params = g_params).json()

print gen['response']
