import json
import os
from glob import glob
from tortoise import Tortoise

current_path = os.path.dirname(os.path.realpath(__file__))


with open(os.path.join(current_path, ".gitignore"), "r", encoding="utf8") as file:
    exclude = set(("src/app/" + file for file in file.read().split("\n") + ["bots", "channels"]))

folders = list(
    set([folder.replace("\\", "/").strip("/") for folder in glob("src/app/*/")]) - exclude
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
    # "apps": {'models': model_paths},
}

TEST_TORTOISE_ORM = {
    "connections": {"default": f"sqlite://{current_path}/db/test/db.sqlite3"},
    "apps": apps,
    # "apps": {'models': model_paths},
}


with open(os.path.join(current_path, "secrets.json")) as file:
    secrets = json.load(file)

SECRET_KEY = secrets.get("SECRET_KEY")
MAIL_PASSWORD = secrets.get("password")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
IS_PROD = os.getenv("IS_PROD", False)
