import spotipy
from spotipy.oauth2 import SpotifyOAuth
from typing import List, Dict


class Spotify:

    def __init__(self):
        scope = "user-library-read"
        self.client = spotipy.Spotify(
            auth_manager=SpotifyOAuth(cache_path='.spotify-cache', scope=scope),
        )

    def get_liked_songs(self, limit: int = 20, page: int = 0) -> Dict:
        return self.client.current_user_saved_tracks(limit=limit, offset=page * limit)
        # print(json.dumps(songs['items'][0], sort_keys=True, indent=4))

    @staticmethod
    def get_searchable_name(song_info: Dict):
        def artist_name(artist_info: Dict):
            return artist_info['name']
        artist_names: str = ' '.join(map(artist_name, song_info['track']['artists']))
        return song_info['track']['name'] + ' ' + artist_names
