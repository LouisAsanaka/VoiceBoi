from spotify import Spotify
from youtube import Youtube
from typing import List, Dict
import vlc

PAGINATION_LIMIT: int = 5


class PlaylistManager:

    def __init__(self):
        self.spotify: Spotify = Spotify()
        self.current_media_list: vlc.MediaList = vlc.get_default_instance().media_list_new()
        self.current_playlist_urls: List[str] = []
        self.current_page: int = -1
        self.total_items: int = 0

    def paginate(self) -> bool:
        if self.current_playlist_urls and len(self.current_playlist_urls) == self.total_items:
            return False
        self.current_page += 1

        response: Dict = self.spotify.get_liked_songs(limit=PAGINATION_LIMIT, page=self.current_page)
        songs: List[Dict] = response['items']
        self.total_items = response['total']
        queries = list(map(Spotify.get_searchable_name, songs))
        print(queries)
        new_urls = list(map(lambda s: Youtube.get_audio_url(Youtube.search(s)[0]), queries))
        print("URLS: ", new_urls)

        self.current_playlist_urls.extend(new_urls)
        self.current_media_list.lock()
        for url in new_urls:
            self.current_media_list.add_media(url)
        self.current_media_list.unlock()
        return True

    def fetch(self, name: str):
        self.current_media_list.release()
        self.current_media_list = vlc.get_default_instance().media_list_new()

        self.current_playlist_urls = []
        self.current_page = -1
        if name == 'liked songs':
            self.paginate()
            return self.current_media_list
        return None
