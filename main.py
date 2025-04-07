from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from core import (
    AICodingAssistant,
    project_manager,
    collaboration,
    code_review,
    terminal,
    version_control
)
import uvicorn

app = FastAPI(title="Enhanced AI Coding Assistant")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

assistant = AICodingAssistant()
projects = project_manager()
collaboration = collaboration()
reviewer = code_review()
terminal = terminal()


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/project")
async def project_view(request: Request):
    project_structure = projects.load_project()
    return templates.TemplateResponse("project.html", {
        "request": request,
        "project_structure": project_structure
    })


@app.websocket("/collab/{room_id}")
async def collaboration_endpoint(websocket: WebSocket, room_id: str):
    await websocket.accept()
    user_id = str(uuid.uuid4())

    try:
        await collaboration.join_room(room_id, user_id, websocket)
        while True:
            data = await websocket.receive_json()
            await collaboration.broadcast(room_id, data, user_id)
    except WebSocketDisconnect:
        await collaboration.leave_room(room_id, user_id)


@app.post("/api/review")
async def code_review(code: str, language: str):
    return reviewer.review_code(code, language)


@app.post("/api/terminal")
async def run_command(command: str):
    return terminal.execute(command)


@app.post("/api/vcs/status")
async def vcs_status():
    vcs = version_control(projects.project_root)
    return vcs.git_status()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)