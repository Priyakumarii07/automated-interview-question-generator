from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from pydantic import BaseModel
import json

from model import generate_questions
from prompt import build_prompt
from schemas import QuestionResponse

app = FastAPI(
    title="Automated Interview Question Generator",
    description="AI-powered system to generate technical interview questions",
    version="1.0" 
)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def serve_frontend():
    return FileResponse("static/index.html")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QuestionRequest(BaseModel):
    role: str
    skills: str
    resume: str
    num_questions: int

@app.post("/generate")
async def generate(req: QuestionRequest):
    data = generate_questions(build_prompt(req))
    validated = QuestionResponse(**data)
    return validated

