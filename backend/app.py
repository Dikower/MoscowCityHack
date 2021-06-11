import shutil
from pathlib import Path
from fastapi import FastAPI
from settings import PROD_TORTOISE_ORM, TEST_TORTOISE_ORM
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from tortoise import Tortoise
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="templates")
CHUNK_SIZE = 1024 * 1024
video_path = Path("video.mp4")

origins = [
    "http://localhost:5000",
    "http://localhost:3000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    shutil.rmtree(
        "db/test"
    )  # Удаляем папку с тестовой базой данных при запуске и импорте

except FileNotFoundError:
    print("Error during delete")
    pass

for path in ["db/test"]:
    Path(path).mkdir(parents=True, exist_ok=True)

config_var = PROD_TORTOISE_ORM


# config_var = TEST_TORTOISE_ORM


@app.on_event("startup")
async def startup():
    await Tortoise.init(config=config_var)
    await Tortoise.generate_schemas(safe=True)
    # await fill_db()


@app.on_event("shutdown")
async def shutdown():
    await Tortoise.close_connections()


if __name__ == '__main__':
    uvicorn.run('app:app', reload=True, use_colors=True)
