import os
import json

"""
Конвертирует аудиофайл в текст, возвращает текст.
На вход подавать путь к .wav файлу.
"""


class AudioModel:
    def __init__(self):
        self.command = 'python run_model.py '

    def upload_file(self, path):
        os.popen(self.command + path)

        with open('res.json', 'r', encoding='utf8') as f:
            d = json.load(f)
            return d['text']
            # return json.dumps({'success': True, 'content': d['text']}), 200, {'ContentType': 'application/json'}
