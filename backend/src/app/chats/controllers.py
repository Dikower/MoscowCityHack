import asyncio
from fastapi import APIRouter, Depends, Cookie, Query, status
from typing import List, Dict, Optional
from fastapi import Request, Response, WebSocket, WebSocketDisconnect
from pymemcache.client import base
from ..users.controllers import oauth2_scheme, get_user
from ..users.models import User
from .models import Chat, ChatType, Message
from ..settings import IS_PROD
from .schemas import Preview

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

    async def get_members(self, user: User, chat_id: str):
        members = self.client.get(chat_id)
        chat = await user.chats.get_or_none(id=chat_id)
        if members is None:
            if chat is None:
                await self.active_connections[user.id].send_json({
                    "status": "error",
                    "reason": f"Chat id: {chat_id} not found"
                })
                return
            # chat =
            members = [member.id for member in await chat.members.all()]
            self.client.set(chat_id, members)
        return members

    async def broadcast(self, user, chat_id, content):
        members = await self.get_members(user, chat_id)
        if members is None:
            return False
        for member in members:
            connection = self.active_connections.get(member, None)
            await connection.send_json(content)
        return True

    async def send_message(self, user: User, to: str, message: dict):
        text = message.get('text', 'Текст-заглушка')
        success = await self.broadcast(user, to, {'event': 'message', 'message': {'text': text}})
        if not success:
            return

        message = await Message.create(sender_id=user.id, chat_id=to, text=text)
        chat = await Chat.get(id=to)  # Checked in get_members
        await chat.messages.add(message)

        
manager = ConnectionManager()


async def get_user_ws(
    websocket: WebSocket,
    session: Optional[str] = Cookie(None)):
    if session is None:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
    return session


@router.websocket("/{token}")
async def websocket_endpoint(websocket: WebSocket,  token: str):
    print(token)
    user = await User.first()
    user_id = user.id
    await manager.connect(websocket, user_id)
    try:
        while True:
            """
            {
                type: message,
                to: chat_id,
                message: {
                    text: Text
                    Message model
                }
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


@router.post('/create', response_model=Preview)
async def create_chat(with_user: str, user=Depends(get_user)):
    another = await User.get_or_none(id=with_user)
    chat = await Chat.create(name=another.fio, type=ChatType.PRIVATE)
    await chat.members.add(user, another)
    return await Preview.from_tortoise_orm(chat)


@router.get('/my', response_model=List[Preview])
async def my_chats(user=Depends(get_user)):
    return await Preview.from_queryset(user.chats.all())


@router.get('/all', response_model=List[Preview])
async def get_chats():
    return await Preview.from_queryset(Chat.all())
