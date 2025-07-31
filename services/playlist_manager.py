# services/playlist_manager.py
def get_all_tracks(playlist_id):
    from services.spotify_auth import get_spotify_client
    sp = get_spotify_client()
    tracks = []
    results = sp.playlist_items(playlist_id)
    tracks.extend(results['items'])
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks

def remove_tracks(playlist_id, uris):
    from services.spotify_auth import get_spotify_client
    sp = get_spotify_client()
    sp.playlist_remove_all_occurrences_of_items(playlist_id, uris)

def create_playlist(user_id, name, public=False):
    from services.spotify_auth import get_spotify_client
    sp = get_spotify_client()
    return sp.user_playlist_create(user=user_id, name=name, public=public)

def add_tracks_to_playlist(playlist_id, track_uris):
    from services.spotify_auth import get_spotify_client
    sp = get_spotify_client()
    sp.playlist_add_items(playlist_id, track_uris)

def search_tracks(query, limit=10):
    from services.spotify_auth import get_spotify_client
    sp = get_spotify_client()
    results = sp.search(q=query, type='track', limit=limit)
    return results['tracks']['items']

def get_user_id():
    from services.spotify_auth import get_spotify_client
    sp = get_spotify_client()
    return sp.current_user()['id']
