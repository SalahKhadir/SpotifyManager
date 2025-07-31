# services/spotify_auth.py
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

# All the scopes we need
SCOPE = "playlist-modify-private playlist-modify-public playlist-read-private"

def get_spotify_client():
    """
    Lazy-load Spotify client so env vars can be set at runtime.
    Supports account switching without restarting the app.
    """
    # Always reload .env in case login page just updated it
    load_dotenv(override=True)

    client_id = os.getenv("SPOTIPY_CLIENT_ID", "").strip()
    client_secret = os.getenv("SPOTIPY_CLIENT_SECRET", "").strip()
    redirect_uri = os.getenv("SPOTIPY_REDIRECT_URI", "").strip()

    if not client_id or not client_secret or not redirect_uri:
        raise Exception("Spotify credentials are missing. Please log in first.")

    # Use a unique cache file for each account so switching works
    cache_path = f".cache-{client_id}"

    return spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope=SCOPE,
            cache_path=cache_path
        )
    )
