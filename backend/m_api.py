import asyncio
from typing import List
from fastapi import FastAPI, BackgroundTasks, WebSocket, WebSocketDisconnect
import threading
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from player import (
    p,
    Song,
)
import ytube_downloader as ytd


app = FastAPI(
    title="Player API",
    description="",
    version="1.0.0",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    servers=[
        {"url": "http://localhost:2407", "description": "Local Development"},
    ],
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def hello():
    return "Player API"


@app.get("/play")
async def play(id: int = 0, resume: bool = False):
    if id >= len(p.playlist):
        return "Song not found"

    if not resume:
        p.stop_music()

    threads = threading.enumerate()
    p.stop_force = True
    try:
        while threads[1].is_alive():
            pass
    except IndexError:
        pass
    print(threading.enumerate())
    p.stop_force = False
    threading.Thread(target=p.play_music, args=(id, resume)).start()
    return p.playlist[id].model_dump()


@app.post("/jumpto")
async def jumpto(req: dict):
    if req["id"] >= len(p.playlist):
        return "Song not found"
    threads = threading.enumerate()
    p.stop_force = True
    try:
        while threads[1].is_alive():
            pass
    except IndexError:
        pass
    print(threading.enumerate())
    p.stop_force = False
    threading.Thread(target=p.jumpto, args=(
        req["id"], False, req["time"])).start()


@app.get("/pause")
async def stop(background_tasks: BackgroundTasks):
    p.pause_music()


@app.websocket("/playlist")
async def ws_playlist(websocket: WebSocket):
    await websocket.accept()
    try:
        data = await websocket.receive_text()
        print(data + " " + "/playlist")
        while True:
            plist = []
            for index, song in enumerate(p.playlist):
                plist.append(song.model_dump())
                if not any(song.playing for song in p.playlist):
                    if p.last_song_id == index:
                        plist[index]["playing"] = True
                plist[index]["id"] = index
            await websocket.send_json({"playlist": plist})
            await asyncio.sleep(3)
    except WebSocketDisconnect:
        print("Client disconnected")


@app.get("/playlist")
async def get_playlist():
    plist = []
    for index, song in enumerate(p.playlist):
        plist.append(song.model_dump())
        plist[index]["id"] = index
    return plist


@app.post("/playlist")
async def post_playlist(new_playlist: List[Song]):
    p.set_playlist(new_playlist)


@app.post("/song")
async def add_song(url: str, background_tasks: BackgroundTasks):
    if url == "":
        return
    await ytd.main(url)
    # asyncio.create_task(ytd.main(url))
    # background_tasks.add_task(ytd.main, url)
    # threading.Thread(target=ytd.main, args=(url,)).start()
    return


@app.delete("/song")
async def delete_song(id: int):
    if p.playlist[id].playing:
        p.stop_music()
        threading.Thread(target=p.play_music, args=(id+1, 0)).start()
    p.playlist.pop(id)


@app.websocket("/position")
async def get_position(websocket: WebSocket):
    await websocket.accept()
    try:
        data = await websocket.receive_text()
        print(data + " " + "/position")
        while True:
            await websocket.send_json({"position": p.get_song_position(), "length": p.get_song_length(), "paused": p.paused})
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        print("Client disconnected")


@app.get("/volume")
async def get_volume():
    return p.get_volume()


@app.post("/volume")
async def set_volume(volume: float):
    p.set_volume(volume)


@app.get("/shuffle")
async def shuffle():
    p.shuffle()


if __name__ == "__main__":
    try:
        uvicorn.run(app, host="0.0.0.0", port=2407)
    except KeyboardInterrupt:
        p.stop_music()
        print("Stopping Server...")
