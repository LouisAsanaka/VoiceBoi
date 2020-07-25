import vlc
from typing import List, Tuple, Dict


class MediaPlayer:

    def __init__(self):
        # i = vlc.Instance('--verbose 9')
        self.i: vlc.Instance = vlc.Instance()
        self.player: vlc.MediaPlayer = self.i.media_player_new()
        self.set_output_device(b'{0.0.0.00000000}.{2aff3d82-88ab-4e00-ab49-b97253d27712}')
        self.list_player: vlc.MediaListPlayer = self.i.media_list_player_new()
        self.list_player.set_media_player(self.player)
        self.callbacks: Dict = {}
        print(self.list_output_devices())

    def register_callback(self, event_type, callback_):
        self.callbacks[event_type] = callback_
        event_manager: vlc.EventManager = self.list_player.event_manager()
        event_manager.event_attach(event_type, callback_)

    def unregister_callback(self, event_type):
        event_manager: vlc.EventManager = self.list_player.event_manager()
        event_manager.event_detach(event_type)

    def list_output_devices(self) -> List[Tuple[bytes, bytes]]:
        """
        Lists the current usable audio output devices.

        :return: List of tuple of the device ID & device description
        """
        devices: List[Tuple[bytes, bytes]] = []
        mods: vlc.AudioOutputDevice = self.player.audio_output_device_enum()
        if mods:
            mod = mods
            while mod:
                mod = mod.contents
                devices.append((mod.device, mod.description))
                mod = mod.next
        vlc.libvlc_audio_output_device_list_release(mods)
        return devices

    def get_player_state(self) -> vlc.State:
        return self.player.get_state()

    def set_output_device(self, device: bytes):
        """
        Sets the audio output device for this media player.

        :param device: the audio output device id
        :return: None
        """
        self.player.audio_output_device_set(module=None, device_id=device)

    def set_audio(self, url: str):
        """
        Sets the audio from the player.

        :param url: an audio URL
        :return: None
        """
        self.set_playlist(self.i.media_list_new([url]))

    def reinitialize_player(self):
        for event_type in self.callbacks.keys():
            self.unregister_callback(event_type)
        self.list_player.release()
        self.list_player = self.i.media_list_player_new()
        self.list_player.set_media_player(self.player)
        for event_type, callback in self.callbacks.items():
            self.register_callback(event_type, callback)

    def set_playlist(self, media_list: vlc.MediaList):
        if media_list.count() == 0:
            return
        self.list_player.set_media_list(media_list)

    def get_volume(self) -> int:
        return self.player.audio_get_volume()

    def set_volume(self, volume: int):
        if volume < 0 or volume > 100:
            return
        self.player.audio_set_volume(volume)

    def play(self):
        """
        Plays the current audio.

        :return: None
        """
        self.set_volume(80)
        self.list_player.play()

    def play_at_index(self, index: int):
        self.set_volume(80)
        self.list_player.play_item_at_index(index)

    def resume(self):
        self.list_player.set_pause(0)

    def pause(self):
        """
        Pauses the current audio.

        :return: None
        """
        self.list_player.set_pause(1)

    def next(self) -> int:
        return self.list_player.next()

    def previous(self) -> int:
        return self.list_player.previous()
