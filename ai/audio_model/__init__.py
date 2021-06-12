from vosk import Model, KaldiRecognizer, SetLogLevel
import sys
import os
import wave
import subprocess

import json
import string

import os
import sys


"""
Конвертирует аудиофайл в текст, возвращает текст.
На вход подавать путь к .wav файлу.
"""


class AudioModel:
    def __init__(self):
        SetLogLevel(0)
        self.sample_rate = 16000
        self.model = Model("model")
        self.rec = KaldiRecognizer(self.model, self.sample_rate)

    def upload_file(self, path):
        process = subprocess.Popen(['ffmpeg', '-loglevel', 'quiet', '-i', path,
                                    '-ar', str(self.sample_rate), '-ac', '1', '-f', 's16le', '-'],
                                   stdout=subprocess.PIPE)

        while True:
            data = process.stdout.read(4000)
            if len(data) == 0:
                break
            if self.rec.AcceptWaveform(data):
                pass
            else:
                pass

        finish = str(self.rec.FinalResult())

        return finish
