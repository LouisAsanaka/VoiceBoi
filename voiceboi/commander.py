from youtube import Youtube
from media_player import MediaPlayer


class Commander:

    def __init__(self):
        self.media_player: MediaPlayer = MediaPlayer()
        self.media_player.set_output_device(self.media_player.list_output_devices()[1][0])
        self.media_player.set_volume(100)

    def play_song(self, query: str):
        audio: str = Youtube.get_audio_url(Youtube.search(query)[0])
        self.media_player.set_audio(audio)
        self.media_player.play()

    def pause_song(self):
        self.media_player.pause()
