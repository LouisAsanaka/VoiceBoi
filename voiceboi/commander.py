from youtube import Youtube
from media_player import MediaPlayer
from playlist_manager import PlaylistManager, PAGINATION_LIMIT
import vlc
from queue import Queue, Empty


class Commander:

    def __init__(self):
        self.media_player: MediaPlayer = MediaPlayer()
        self.media_player.set_output_device(self.media_player.list_output_devices()[1][0])
        self.media_player.set_volume(100)

        self.is_playing_playlist: bool = False
        self.playlist_manager: PlaylistManager = PlaylistManager()

        self.paginate_playlist_queue: Queue = Queue()

        def paginate_callback(event):
            self.paginate_playlist_queue.put('')
            print('queuing pagination')

        self.media_player.register_callback(
            vlc.EventType.MediaListPlayerPlayed, paginate_callback
        )

    def play_song(self, query: str):
        self.is_playing_playlist = False

        audio: str = Youtube.get_audio_url(Youtube.search(query)[0])
        self.media_player.set_audio(audio)
        self.media_player.play()

    def resume_song(self):
        self.media_player.resume()

    def pause_song(self):
        self.media_player.pause()

    def next_song(self):
        self.media_player.next()
        # if self.is_playing_playlist and self.media_player.next() == -1:
        #     self._paginate_and_continue()

    def previous_song(self):
        self.media_player.previous()

    def play_playlist(self, name: str):
        name = name.lower()
        if name == 'liked songs':
            self.is_playing_playlist = True
            songs = self.playlist_manager.fetch(name)
            if songs is None:
                return
            self._reinitialize_player(from_start=True)

    def loop(self):
        try:
            self.paginate_playlist_queue.get(block=False)
            self._paginate_and_continue()
        except Empty:
            pass

    def _paginate_and_continue(self):
        self.playlist_manager.paginate()
        self._reinitialize_player(from_start=False)

    def _reinitialize_player(self, from_start: bool = True):
        self.media_player.pause()
        self.media_player.reinitialize_player()
        self.media_player.set_playlist(self.playlist_manager.current_media_list)
        if from_start:
            self.media_player.play()
        else:
            index = self.playlist_manager.current_media_list.count() - PAGINATION_LIMIT
            self.media_player.play_at_index(index)
