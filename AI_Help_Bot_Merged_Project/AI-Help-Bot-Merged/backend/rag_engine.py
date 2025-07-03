import re
from pathlib import Path
import pickle, faiss, torch
from sentence_transformers import SentenceTransformer
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline

# Settings
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
GEN_MODEL   = "MBZUAI/LaMini-Flan-T5-248M"
TOP_K       = 6
DEVICE      = "cpu"

# Load components
embedder = SentenceTransformer(EMBED_MODEL, device=DEVICE)
index    = faiss.read_index("data/processed/faiss.index")
meta     = pickle.load(open("data/processed/doc_metadata.pkl", "rb"))

tokenizer = AutoTokenizer.from_pretrained(GEN_MODEL)
model     = AutoModelForSeq2SeqLM.from_pretrained(GEN_MODEL, torch_dtype=torch.float32)
generator = pipeline("text2text-generation", model=model, tokenizer=tokenizer, device=0 if DEVICE == "cuda" else -1)

def retrieve(query: str, k: int = TOP_K):
    q_emb = embedder.encode([query])
    sim, ids = index.search(q_emb, k)
    return [meta[i]["text"] for i in ids[0]]

def build_prompt(query: str, ctx: list[str]):
    system = (
        "You are an intelligent and friendly assistant like ChatGPT. "
        "Your job is to help users understand information from MOSDAC satellite data. "
        "Answer naturally and clearly. Add extra detail if the question is vague."
    )
    context = "\n".join(f"- {c.strip()}" for c in ctx if c.strip())
    return f"""{system}

Context:
{context}

User: {query}
Assistant:"""

def is_greeting(msg: str) -> bool:
    return msg.lower().strip() in {"hi", "hello", "hey", "hai", "good morning", "good evening"}

def answer(query: str) -> str:
    if is_greeting(query):
        return "Hello! 👋 I'm here to help you with anything related to MOSDAC satellite data, ISRO missions, or weather products. What would you like to ask?"

    ctx = retrieve(query)
    prompt = build_prompt(query, ctx)
    response = generator(prompt, max_new_tokens=200, do_sample=False)[0]["generated_text"]
    return response.strip()
