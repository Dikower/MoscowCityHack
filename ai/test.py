from audio_model import AudioModel
from time import sleep

am = AudioModel()
sleep(1)
print(am.upload_file('Test.wav'))
