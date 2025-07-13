from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List
import os
from rag_pipeline import RAGPipeline
from config import set_cors

app = FastAPI()
set_cors(app)

UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

pipeline = None
if any(f.endswith((".pdf", ".png", ".jpg", ".jpeg")) for f in os.listdir(UPLOAD_DIR)):
    pipeline = RAGPipeline(UPLOAD_DIR)

@app.get("/")
def home():
    return {"message": "📘 Knowledge Bot is ready!"}

@app.post("/upload/")
async def upload_files(files: List[UploadFile] = File(...)):
    for file in files:
        filepath = os.path.join(UPLOAD_DIR, file.filename)
        with open(filepath, "wb") as f:
            f.write(await file.read())

    global pipeline
    pipeline = RAGPipeline(UPLOAD_DIR)
    return {"message": "✅ Files uploaded and indexed."}

class Question(BaseModel):
    question: str

class Answer(BaseModel):
    answer: str

@app.post("/ask", response_model=Answer)
async def ask_question(q: Question):
    if pipeline is None or pipeline.chain is None:
        raise HTTPException(status_code=400, detail="❌ Pipeline not initialized.")
    answer = pipeline.ask(q.question)
    return Answer(answer=answer)
