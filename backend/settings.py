import os
from glob import glob
import json

with open('.gitignore', 'r', encoding='utf8') as file:
    exclude = set(file.read().split('\n'))

folders = list(set([folder.strip('\\').strip('/') for folder in glob("*/")]) - exclude)

apps = {folder: {'models': [f'{folder}.models']} for folder in folders}
PROD_TORTOISE_ORM = {
    'connections': {'default': 'sqlite://db/prod/db.sqlite3'},
    'apps': apps
}

TEST_TORTOISE_ORM = {
    'connections': {'default': 'sqlite://db/test/db.sqlite3'},
    'apps': apps
}


with open('secrets.json') as file:
    SECRET_KEY = json.load(file)
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30
