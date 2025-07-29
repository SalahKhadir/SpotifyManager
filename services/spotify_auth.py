
import os
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

def get_spotify_client():
    return Spotify(auth_manager=SpotifyOAuth(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
        scope="playlist-read-private playlist-modify-public playlist-modify-private"
    ))
