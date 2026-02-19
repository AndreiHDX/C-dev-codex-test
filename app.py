from __future__ import annotations

import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import DefaultDict

from flask import Flask, send_from_directory
from flask_sock import Sock

app = Flask(__name__, static_folder="static", template_folder="templates")
sock = Sock(app)

BASE_DIR = Path(__file__).parent

# Храним активные подключения по комнатам (в памяти процесса).
rooms: DefaultDict[str, set] = defaultdict(set)


def now_time() -> str:
    return datetime.now().strftime("%H:%M")


def broadcast(room: str, payload: dict) -> None:
    dead_connections = []
    for ws in rooms[room]:
        try:
            ws.send(json.dumps(payload, ensure_ascii=False))
        except Exception:
            dead_connections.append(ws)

    for ws in dead_connections:
        rooms[room].discard(ws)


@app.get("/")
def index() -> tuple[str, int] | str:
    return send_from_directory(BASE_DIR / "templates", "index.html")


@sock.route("/ws")
def websocket(ws) -> None:
    username = None
    room = None

    while True:
        raw = ws.receive()
        if raw is None:
            break

        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            ws.send(json.dumps({"type": "error", "message": "Некорректный JSON."}, ensure_ascii=False))
            continue

        action = data.get("action")

        if action == "join":
            candidate_name = str(data.get("username", "")).strip()
            candidate_room = str(data.get("room", "")).strip() or "general"

            if not candidate_name:
                ws.send(json.dumps({"type": "error", "message": "Введите имя пользователя."}, ensure_ascii=False))
                continue

            username = candidate_name
            room = candidate_room
            rooms[room].add(ws)
            broadcast(
                room,
                {
                    "type": "system",
                    "message": f"{username} присоединился к комнате #{room}",
                    "time": now_time(),
                },
            )
            continue

        if action == "message":
            if not username or not room:
                ws.send(json.dumps({"type": "error", "message": "Сначала подключитесь к комнате."}, ensure_ascii=False))
                continue

            text = str(data.get("text", "")).strip()
            if not text:
                continue

            broadcast(
                room,
                {
                    "type": "chat",
                    "username": username,
                    "text": text,
                    "time": now_time(),
                },
            )
            continue

        ws.send(json.dumps({"type": "error", "message": "Неизвестное действие."}, ensure_ascii=False))

    if room and ws in rooms[room]:
        rooms[room].discard(ws)
        if username:
            broadcast(
                room,
                {
                    "type": "system",
                    "message": f"{username} покинул комнату #{room}",
                    "time": now_time(),
                },
            )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
