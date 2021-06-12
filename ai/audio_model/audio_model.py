import os
import json


class AudioModel:

    def __init__(self):
        self.command = 'python run_model.py '

    def upload_file(self, path):
        os.popen(self.command + path)

        with open('res.json') as f:
            d = json.load(f)
            return json.dumps({'success': True, 'content': d['text']}), 200, {'ContentType': 'application/json'}
