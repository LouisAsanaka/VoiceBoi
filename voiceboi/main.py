from dotenv import load_dotenv
load_dotenv()

import vlc
from youtube import Youtube
from commander import Commander
from voice_recognition import VoiceRecognition
import time


def main():
    commander: Commander = Commander()

    voice_recognition = VoiceRecognition(commander)
    voice_recognition.start_recognizer()
    input('Press enter to quit\n')


if __name__ == '__main__':
    main()
