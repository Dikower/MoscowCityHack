import asyncio
from fastapi import APIRouter, Depends
from typing import List, Dict
from fastapi import Request, Response, WebSocket, WebSocketDisconnect
from pymemcache.client import base
from ..users.controllers import oauth2_scheme, get_user
from ..users.models import User
from .models import Chat
from ..settings import IS_PROD
router = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, WebSocket] = {}

        host = 'localhost'
        if IS_PROD:
            host = 'memcached'
        # memcached client
        self.client = base.Client((host, 11211))

    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id):
        del self.active_connections[user_id]

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast_message(self, user, to, message):
        chat = self.client.get(to)
        if chat is None:
            chat = await user.chats.get_or_none(id=to)
            if chat is None:
                await self.active_connections[user.id].send_json({
                    "status": "error",
                    "reason": f"Chat id: {to} not found"
                })
            # chat =

        members = [member.id for member in await chat.members.all()]
        print(members)

        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@router.websocket("/")
async def websocket_endpoint(websocket: WebSocket, user: User = Depends(get_user)):
    user_id = user.id
    await manager.connect(websocket, user_id)
    try:
        while True:
            """
            {
                type: message,
                to: chat_id,
                message: Message model
            }
            {
                type: event
                to: chat_id
            }
            """
            data = await websocket.receive_json()
            if data['type'] == 'message':
                to, message = data['to'], data['message']
                await manager.broadcast_message(user, to, message)

    except WebSocketDisconnect:
        manager.disconnect(user_id)
        # await manager.broadcast(f"Client #{client_id} left the chat")
        print('Disconnected')


@router.get('/all')
async def get_chats():
    ...
