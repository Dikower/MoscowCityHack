import shutil
from pathlib import Path
from fastapi import FastAPI
from settings import PROD_TORTOISE_ORM, TEST_TORTOISE_ORM
from fastapi.middleware.cors import CORSMiddleware
from tortoise import Tortoise
import uvicorn
from rich.console import Console, COLOR_SYSTEMS
from users.controllers import router as user_router

# print(COLOR_SYSTEMS)
console = Console(color_system='windows')

app = FastAPI()

origins = [
    'http://localhost:5000',
    'http://localhost:3000',
    'http://localhost:8000',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

try:
    shutil.rmtree(
        'db/test'
    )  # Удаляем папку с тестовой базой данных при запуске и импорте

except FileNotFoundError:
    print('Error during delete')
    pass

for path in ['db/test']:
    Path(path).mkdir(parents=True, exist_ok=True)

# config_var = PROD_TORTOISE_ORM
config_var = TEST_TORTOISE_ORM

app.include_router(user_router, prefix='/users', tags=['Users'])


@app.on_event('startup')
async def startup():
    try:
        await Tortoise.init(config=config_var)
        await Tortoise.generate_schemas(safe=True)
    except Exception as ex:
        print(ex)
    # await fill_db()


@app.on_event('shutdown')
async def shutdown():
    await Tortoise.close_connections()

if __name__ == '__main__':
    uvicorn.run('app:app', reload=True, use_colors=True)
