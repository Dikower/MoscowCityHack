import json
import os
from glob import glob

current_path = os.path.dirname(os.path.realpath(__file__))


with open(os.path.join(current_path, ".gitignore"), "r", encoding="utf8") as file:
    exclude = set(("src/hack_backend/" + file for file in file.read().split("\n")))

folders = list(
    set([folder.strip("\\").strip("/") for folder in glob("src/hack_backend/*/")])
    - exclude
)


apps = {
    folder.rsplit("/", maxsplit=1)[1]: {
        "models": [f"{folder.replace('/', '.').replace('src.', '')}.models"]
    }
    for folder in folders
}
PROD_TORTOISE_ORM = {
    "connections": {"default": f"sqlite://{current_path}/db/prod/db.sqlite3"},
    "apps": apps,
}

TEST_TORTOISE_ORM = {
    "connections": {"default": f"sqlite://{current_path}/db/test/db.sqlite3"},
    "apps": apps,
}


with open(os.path.join(current_path, "secrets.json")) as file:
    SECRET_KEY = json.load(file)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
