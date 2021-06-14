from fastapi import FastAPI
from uvicorn import run

from pydantic import BaseModel

from text_model import TextModel

app = FastAPI()

text_ml = None


class Message(BaseModel):
    msg: str


@app.on_event("startup")
async def startup_event():
    global text_ml
    text_ml = TextModel()


@app.post("/message_info")
async def message_info(message: Message):
    info = text_ml.user_msg(message.msg)
    return info


if __name__ == "__main__":
    run(app, host="0.0.0.0", use_colors=True, port=8001)
