from fastapi import FastAPI
from dotenv import load_dotenv
from pydantic import BaseModel
from fastapi.routing import APIRoute 
import jaclang 
  # allows loading .jac files directly


# Load the jac file
from .import generate_poem as poem_mod # this imports generate_poem.jac





# Load environment variables from .env file
load_dotenv()

import os
print("Gemini API key found:", os.getenv("GEMINI_API_KEY") is not None)


app = FastAPI(title="Jac Poem API")

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/")
def list_routes():
    return {"routes": [f"{r.path} {list(r.methods)}" for r in app.routes if isinstance(r, APIRoute)]}

class PoemRequest(BaseModel):
    subject: str
    person_for: str
    title: str

@app.post("/generate_poem")
def generate_poem_endpoint(req: PoemRequest):   # <- different name to avoid clash
    poem = poem_mod.generate_poem(req.subject, req.person_for, req.title)
    return {
        "title": poem.title,
        "subject": poem.subject,
        "person_for": poem.person_for,
        "body": poem.body,
    }