from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.rag_engine import answer

class Query(BaseModel):
    query: str

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.post("/generate")
def generate(q: Query):
    return {"answer": answer(q.query)}

@app.get("/ping")
def ping():
    return {"status":"ok"}
