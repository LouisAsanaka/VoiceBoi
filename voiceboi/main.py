from dotenv import load_dotenv
load_dotenv()

from commander import Commander
from voice_recognition import VoiceRecognition
import time


def main():
    commander: Commander = Commander()
    # commander.play_playlist('liked songs')
    # time.sleep(3)
    # commander.next_song()
    # commander.media_player.player.set_position(0.9)

    voice_recognition = VoiceRecognition(commander)
    voice_recognition.start_recognizer()

    while True:
        commander.loop()
        voice_recognition.loop()
        time.sleep(0.2)


if __name__ == '__main__':
    main()
