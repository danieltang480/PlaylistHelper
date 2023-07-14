import spotipy
from spotipy.oauth2 import SpotifyOAuth
import random

# Set up the Spotify API credentials
scope = "playlist-modify-public"
client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"
redirect_uri = "http://localhost:8888/callback"  # Make sure to add this as a Redirect URI in your Spotify Developer Dashboard

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri))

# Get the user's playlists
playlists = sp.current_user_playlists()["items"]

# Display the playlists and let the user select one
print("Your playlists:")
for i, playlist in enumerate(playlists):
    print(f"{i+1}. {playlist['name']}")

selected_index = int(input("Select a playlist by entering its number: ")) - 1
selected_playlist = playlists[selected_index]

# Fetch the tracks for the selected playlist
tracks = sp.playlist_tracks(selected_playlist['id'])
playlist_tracks = tracks['items']

# Select a random track from the playlist as the seed track
random_track = random.choice(playlist_tracks)
seed_track_id = random_track['track']['id']

# Prompt the user for the number of songs to add
num_songs = int(input("Enter the number of songs to add: "))

# Get song recommendations based on the selected playlist
recommendations = sp.recommendations(seed_tracks=[seed_track_id], limit=num_songs)

# Add the recommended songs to the playlist
track_uris = [track['uri'] for track in recommendations['tracks']]
sp.playlist_add_items(selected_playlist['id'], track_uris)

print(f"{num_songs} songs have been added to your playlist '{selected_playlist['name']}'!")
