import shutil
from pathlib import Path
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from rich.console import COLOR_SYSTEMS, Console
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise

from .settings import PROD_TORTOISE_ORM, TEST_TORTOISE_ORM
from .users.controllers import router as user_router

# print(COLOR_SYSTEMS)
console = Console(color_system="windows")

origins = [
    "http://localhost:5000",
    "http://localhost:3000",
    "http://localhost:8000",
]

# config_var = PROD_TORTOISE_ORM
config_var = TEST_TORTOISE_ORM

# Tortoise.init_models([".users.models"], "models")


def prepare_db():
    # Удаляем папку с тестовой базой данных при запуске и импорте
    current_path = os.path.dirname(os.path.realpath(__file__))
    test_db_path = os.path.join(current_path, "db", "test")
    try:
        shutil.rmtree(test_db_path)
    except FileNotFoundError:
        print("Error during delete")

    for path in [test_db_path]:
        Path(path).mkdir(parents=True, exist_ok=True)


async def startup():
    try:
        pass
        # await Tortoise.init(config=config_var)
        # await Tortoise.generate_schemas(safe=True)
    except Exception as ex:
        print(ex)
    # await fill_db()


async def shutdown():
    await Tortoise.close_connections()


def create_app():

    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    prepare_db()

    Tortoise.init_models(
        [
            "app.users.models"
        ],
        "models",
    )

    register_tortoise(
        app,
        db_url="sqlite://src/app/db/test/db.sqlite3",
        modules={
            "models": [
                "app.users.models"
            ],
        },
        generate_schemas=True,
        add_exception_handlers=True,
    )

    app.include_router(user_router, prefix="/users", tags=["Users"])

    app.add_event_handler("startup", startup)
    app.add_event_handler("shutdown", shutdown)

    return app
