from typing import Dict, List
import uuid
from fastapi import WebSocket


class CollaborationManager:
    def __init__(self):
        self.rooms: Dict[str, Dict[str, WebSocket]] = {}
        self.cursors: Dict[str, Dict] = {}

    async def join_room(self, room_id: str, user_id: str, websocket: WebSocket):
        """Add user to a collaboration.js room"""
        if room_id not in self.rooms:
            self.rooms[room_id] = {}
        self.rooms[room_id][user_id] = websocket
        self.cursors[user_id] = {"position": 0, "color": self._generate_color()}

    async def leave_room(self, room_id: str, user_id: str):
        """Remove user from a collaboration.js room"""
        if room_id in self.rooms and user_id in self.rooms[room_id]:
            del self.rooms[room_id][user_id]
            del self.cursors[user_id]

    async def broadcast(self, room_id: str, message: Dict, sender_id: str = None):
        """Send message to all users in a room"""
        if room_id in self.rooms:
            for user_id, websocket in self.rooms[room_id].items():
                if user_id != sender_id:
                    await websocket.send_json(message)

    def _generate_color(self) -> str:
        """Generate a random color for user cursor"""
        colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#FFA07A", "#98D8C8"]
        return colors[len(self.cursors) % len(colors)]