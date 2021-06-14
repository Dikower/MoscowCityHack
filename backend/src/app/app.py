import os
import json
import shutil
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from rich.console import COLOR_SYSTEMS, Console
from tortoise import Tortoise
from randomuser import RandomUser
from .settings import PROD_TORTOISE_ORM, TEST_TORTOISE_ORM, IS_PROD
from .users.controllers import router as user_router
from .chats.controllers import router as chat_router
from .users.models import User
from .chats.models import Chat, ChatType, Message


# print(COLOR_SYSTEMS)
console = Console(color_system="windows")

origins = ["*"]

config_var = PROD_TORTOISE_ORM
# config_var = TEST_TORTOISE_ORM


def prepare_db():
    # Удаляем папку с тестовой базой данных при запуске и импорте
    current_path = os.path.dirname(os.path.realpath(__file__))
    test_db_path = os.path.join(current_path, "db", "test")
    prod_db_path = os.path.join(current_path, "db", "prod")
    try:
        shutil.rmtree(test_db_path)
    except FileNotFoundError:
        print("Error during delete")

    for path in [test_db_path, prod_db_path]:
        Path(path).mkdir(parents=True, exist_ok=True)


async def startup():
    try:
        await Tortoise.init(config=config_var)
        await Tortoise.generate_schemas(safe=True)
    except Exception as ex:
        print(ex)

    users = [
        {
            'avatar': user.get_picture(),
            'fio': user.get_full_name(),
            'email': user.get_email()
        } for user in RandomUser.generate_users(10)
    ]

    with open('users.json', 'r', encoding='utf8') as file:
        users = json.load(file)

    test_user = users[0]
    # with open('users.json', 'w', encoding='utf8') as file:
        # json.dump(users, file, ensure_ascii=False, indent=2)
    print(test_user)
    user_inst = []

    # for user in users:
    #     user_inst.append(await User.create(**user))
    # user = await User.get_or_none(email=test_user['email'])
    # for user2 in user_inst:
    #     chat = await Chat.create(name=user2.fio, type=ChatType.PRIVATE, avatar=user2.avatar)
    #     await chat.members.add(user, user2)
    #     await Message.create(sender=user, chat=chat, text=f'Привет, {user2.fio}! 🤩')
    #     await Message.create(sender=user2, chat=chat, text=f'Привет, {user.fio}!')
    #     await Message.create(sender=user, chat=chat, text=f'Как твои дела?')
    #     await Message.create(sender=user2, chat=chat, text=f'Хоорошо, спасибо 😄')


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
    app.include_router(chat_router, prefix="/chats", tags=["Chats"])

    app.add_event_handler("startup", startup)
    app.add_event_handler("shutdown", shutdown)

    if IS_PROD:
        console.print('Docs link: https://b.sberchat.hackmasters.tech/docs', style='bold blue')
    else:
        console.print('Docs link: http://localhost:8000/docs', style='bold blue')

    return app
