import spotipy
import os
import sys
import json
import webbrowser
from spotipy.oauth2 import SpotifyOAuth
from json.decoder import JSONDecodeError



# Credentials
cid = '1ea7d06fffe8424b865d04a3cb9babbd'
cs = '2477749e29e241bda5a79ad82eca83d6'
r_uri = 'https://google.com/'

# Username and browser authorization
scope = 'user-read-private user-read-playback-state user-modify-playback-state'

# Create Spotify object
spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cid, client_secret=cs, scope=scope, redirect_uri=r_uri))

# Display device Spotify is playing on
devices = spotify.devices()
print(json.dumps(devices, sort_keys=True, indent=4))
deviceID = devices['devices'][0]['id']

# Track information
track = spotify.current_user_playing_track()
print(json.dumps(track, sort_keys=True, indent=4))
print()
artist = track['item']['artists'][0]['name']
track = track['item']['name']

if track != "":
    print('Currently playing ' + artist + ' - ' + track)

# User info
user = spotify.current_user()
displayName = user['display_name']
follower = user['followers']['total']

while True:
    print()
    print('>>> Welcome to Spotify ' + displayName + '!')
    print(">>> You have " + str(follower) + ' followers.')
    print()
    print('0 - Search for an artist')
    print('1 - exit')
    print()
    choice = input("Enter your selection: ")

    # Search artist
    if choice == '0':
        print()
        search_query = input("Enter the artist's name: ")
        print()

        # Get search results
        search_results = spotify.search(search_query, 1, 0, 'artist')

        # Display artist details
        artist = search_results['artists']['items'][0]
        print(artist['name'])
        print(str(artist['followers']['total']) + ' followers')
        print(artist['genres'][0])
        print()
        webbrowser.open(artist['images'][0]['url'])
        artist_ID = artist['id']

        # Get album details
        track_URIs = []
        track_art = []
        z = 0

        # Extract album data
        album_results = spotify.artist_albums(artist_ID)
        album_results = album_results['items']

        for item in album_results:
            print('ALBUM: ' + item['name'])
            album_ID = item['id']
            album_art = item['images'][0]['url']

            # Extract track data
            track_results = spotify.album_tracks(album_ID)
            track_results = track_results['items']

            for item in track_results:
                print(str(z) + ': ' + item['name'])
                track_URIs.append(item['uri'])
                track_art.append(album_art)
                z += 1
            print()

        # Display album art
        while True:
            song_selection = input('Enter a song number to play (Enter "x" to select another artist): ')
            if song_selection == 'x':
                break
            track_selection_list = [track_URIs[int(song_selection)]]
            spotify.start_playback(deviceID, None, track_selection_list)
            webbrowser.open(track_art[int(song_selection)])

    if choice == '1':
        break
