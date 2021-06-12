import asyncio
from fastapi import APIRouter
from fastapi import Request, Response, WebSocket

router = APIRouter()


@router.websocket("/")
async def websocket_endpoint(path: str, websocket: WebSocket):
    await websocket.accept()
    i = 0
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")


@router.get('/all')
async def get_chats():
    ...
