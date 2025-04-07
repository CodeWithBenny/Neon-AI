from fastapi import FastAPI
from core import AICodingAssistant

app = FastAPI()
assistant = AICodingAssistant()

@app.post("/complete")
async def complete_code(code: str, language: str = "python"):
    return {"suggestions": assistant.completer.complete(code, language)}

@app.post("/debug")
async def debug_code(code: str, error: str, language: str = "python"):
    return assistant.debugger.analyze(code, error, language)

@app.post("/explain")
async def explain_code(code: str, language: str = "python"):
    return {"explanation": assistant.explainer.explain(code, language)}

# Additional endpoints for other features...