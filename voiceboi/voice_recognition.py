import speech_recognition as sr
from pocketsphinx.pocketsphinx import Decoder
from commander import Commander
from tts import TTS
import os
from queue import Queue

keywords = [
    ("okay google", 1e-4)
]


class VoiceRecognition:

    def __init__(self, commander: Commander):
        self.r = sr.Recognizer()
        self.commander: Commander = commander
        self.tts_engine: TTS = TTS()

        self.listen_command_queue: Queue = Queue()
        self.listening_for_command: bool = False

    def listen_for_hotword(self, recognizer: sr.Recognizer, audio: sr.AudioData):
        """
        Callback that runs continuously in the background to listen
        for hotwords using offline speech recognition.

        :param recognizer: the Recognizer instance
        :param audio: audio data to analyze
        :return: None
        """
        if self.listening_for_command:
            return
        try:
            speech_as_text: Decoder = recognizer.recognize_sphinx(audio, keyword_entries=keywords)
            print(f"Heard '{speech_as_text}'")

            for keyword, sensitivity in keywords:
                if keyword in speech_as_text:
                    self.listen_command_queue.put('command')
                    break
        except sr.UnknownValueError:
            print("Oops! Didn't catch that")

    def listen_for_command(self):
        """
        Listens for commands using online speech recognition.

        :return: None
        """
        print("Listening for command...")
        try:
            with sr.Microphone() as source:
                audio_data = self.r.listen(source)
                command: str = self.r.recognize_google(
                    audio_data, key=os.environ['GOOGLE_API_KEY']).lower()
                print(f"Heard command: '{command}'")
                split_command = command.split(' ')
                if split_command[0] == 'play':
                    self.tts_engine.say("Playing song")
                    if len(split_command) == 1:
                        self.commander.pause_song()
                    else:
                        self.commander.play_song(query=' '.join(split_command[1:]))
                elif split_command[0] == 'pause' or split_command[0] == 'stop':
                    self.tts_engine.say("Pausing song")
                    self.commander.pause_song()
        except sr.UnknownValueError:
            print("Oops! Didn't catch that")
            self.tts_engine.say("Oops! Didn't catch that")

    def start_recognizer(self):
        with sr.Microphone() as source:
            self.r.adjust_for_ambient_noise(source)
            print("Done calibrating!")
            print(self.r.energy_threshold)
        self.r.dynamic_energy_threshold = False
        # self.r.energy_threshold = 800
        self.r.listen_in_background(sr.Microphone(), self.listen_for_hotword)
        while True:
            self.listen_command_queue.get(block=True)

            self.listening_for_command = True
            self.listen_for_command()
            self.listening_for_command = False
