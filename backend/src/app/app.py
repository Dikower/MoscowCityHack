import shutil
from pathlib import Path
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from rich.console import COLOR_SYSTEMS, Console
from tortoise import Tortoise
from randomuser import RandomUser
from .settings import PROD_TORTOISE_ORM, TEST_TORTOISE_ORM, IS_PROD
from .users.controllers import router as user_router
from .users.models import User


# print(COLOR_SYSTEMS)
console = Console(color_system="windows")

origins = [
    "http://localhost:5000",
    "http://localhost:3000",
    "http://localhost:8000",
]

# config_var = PROD_TORTOISE_ORM
config_var = TEST_TORTOISE_ORM


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
        await Tortoise.init(config=config_var)
        await Tortoise.generate_schemas(safe=True)
    except Exception as ex:
        print(ex)

    if not IS_PROD:
        users = [
            {
                'avatar': user.get_picture(),
                'fio': user.get_full_name(),
                'email': user.get_email()
            } for user in RandomUser.generate_users(10)
        ]
        for user in users:
            await User.create(**user)


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

    app.include_router(user_router, prefix="/users", tags=["Users"])

    app.add_event_handler("startup", startup)
    app.add_event_handler("shutdown", shutdown)

    if IS_PROD:
        console.print('Docs link: https://b.sberchat.hackmasters.tech/docs', style='bold blue')
    else:
        console.print('Docs link: http://localhost:8000/docs', style='bold blue')

    return app
