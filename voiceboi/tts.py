import pyttsx3
import time


class TTS:

    def __init__(self):
        self.tts_engine: pyttsx3.Engine = pyttsx3.init(debug=True)

    def say(self, text: str):
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()
