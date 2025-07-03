"""
Ingest EVERYTHING in data/raw/ (html, pdf, docx, xlsx, txt) ➜
chunk ➜ embed ➜ save FAISS index + metadata.
"""

from pathlib import Path
import re, pickle, json, fitz, docx2txt, pandas as pd, faiss

from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer

RAW_DIR  = Path("data/raw")
PROC_DIR = Path("data/processed"); PROC_DIR.mkdir(parents=True, exist_ok=True)
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
CHUNK_SIZE  = 600            # characters
STRIDE      = 100            # overlap

embedder = SentenceTransformer(EMBED_MODEL)
index    = faiss.IndexFlatIP(embedder.get_sentence_embedding_dimension())
meta     = []

def clean(text:str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    return text

def chunk_text(text:str):
    for i in range(0, len(text), CHUNK_SIZE - STRIDE):
        yield text[i:i+CHUNK_SIZE]

def read_html(fp):
    return clean(BeautifulSoup(fp.read_text(encoding="utf-8", errors="ignore"), "html.parser").get_text(" "))

def read_pdf(fp):   return clean(" ".join(page.get_text() for page in muPDF.open(fp)))
def read_docx(fp):  return clean(docx2txt.process(fp))
def read_xlsx(fp):
    dfs = pd.read_excel(fp, sheet_name=None)
    return clean(" ".join(df.to_string(index=False) for df in dfs.values()))
def read_txt(fp):   return clean(fp.read_text())

READERS = {".html":read_html, ".htm":read_html, ".pdf":read_pdf,
           ".docx":read_docx, ".xlsx":read_xlsx, ".txt":read_txt}

def ingest_one(fp:Path, doc_id:int):
    text = READERS[fp.suffix.lower()](fp)
    for chunk in chunk_text(text):
        emb = embedder.encode([chunk])
        index.add(emb)
        meta.append({"id": doc_id, "file": fp.name, "text": chunk})
    return len(meta)

doc_id = 0
for fp in RAW_DIR.rglob("*"):
    if fp.suffix.lower() in READERS:
        doc_id = ingest_one(fp, doc_id) + 1
        print(f"Ingested: {fp}")

faiss.write_index(index, str(PROC_DIR / "faiss.index"))
pickle.dump(meta, open(PROC_DIR / "doc_metadata.pkl","wb"))
print(f"✅  Done. Total chunks: {len(meta)}")
