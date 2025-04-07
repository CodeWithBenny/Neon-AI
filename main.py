from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from core import AICodingAssistant
import uvicorn
import re

app = FastAPI(title="Neon AI Coding Assistant")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

assistant = AICodingAssistant()


def detect_language(code: str) -> str:
    """Auto-detect programming language from code snippets"""
    patterns = {
        'python': (r'\b(def|import|from|__init__|lambda)\b',
                   r'^\s*(#|""")'),
        'javascript': (r'\b(function|let|const|=>|require\(|export)\b',
                       r'^\s*(//|/\*)'),
        'java': (r'\b(public\s+class|import\s+java\.|System\.out\.print)\b',
                 r'^\s*(//|/\*)'),
        'c': (r'#include\s+<|printf\(|->|struct\s+\w+\s*\{',
              r'^\s*(//|/\*)'),
        'cpp': (r'#include\s+<|std::|using\s+namespace|template\s*<',
                r'^\s*(//|/\*)')
    }

    for lang, (keywords, comments) in patterns.items():
        if re.search(keywords, code) or re.search(comments, code, re.MULTILINE):
            return lang
    return "python"  # default


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            action = data.get("action")
            code = data.get("code", "")

            # Auto-detect language if not specified
            language = data.get("language") or detect_language(code)

            if action == "complete":
                suggestions = assistant.completer.complete(code, language)
                await websocket.send_json({
                    "type": "suggestions",
                    "data": suggestions,
                    "detected_language": language
                })

            elif action == "explain":
                explanation = assistant.explainer.explain(code, language)
                await websocket.send_json({
                    "type": "explanation",
                    "data": explanation,
                    "detected_language": language
                })

    except WebSocketDisconnect:
        print("Client disconnected")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)