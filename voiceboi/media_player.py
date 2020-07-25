import vlc
from typing import List, Tuple


class MediaPlayer:

    def __init__(self):
        # i = vlc.Instance('--verbose 9')
        self.i = vlc.Instance()
        self.player: vlc.MediaPlayer = self.i.media_player_new()

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
        self.player.set_mrl(url)

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
        self.player.play()

    def pause(self):
        """
        Pauses the current audio.

        :return: None
        """
        self.player.pause()
