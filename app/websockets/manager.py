from collections import defaultdict
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self._connections: dict[int, list[WebSocket]] = defaultdict(list)

    async def connect(self, user_id: int, websocket: WebSocket):
        await websocket.accept()
        self._connections[user_id].append(websocket)

    def disconnect(self, user_id: int, websocket: WebSocket):
        self._connections[user_id].remove(websocket)
        if not self._connections[user_id]:
            del self._connections[user_id]

    async def send_to_user(self, user_id: int, payload: dict):
        for ws in self._connections.get(user_id, []):
            await ws.send_json(payload)

    def is_connected(self, user_id: int) -> bool:
        return bool(self._connections.get(user_id))