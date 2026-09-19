import os
import hashlib
import sqlite3

from pypdf import PdfReader

from app.services.vector_store import VectorStore
from app.services.ollama_provider import get_embeddings

DB_PATH = "app/support_bot.db"
INGEST_TABLE = "ingested_files"

vector_store = VectorStore()


# ---------------------------
# DB INIT FOR INGEST TRACKING
# ---------------------------

def init_ingestion_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute(f"""
        CREATE TABLE IF NOT EXISTS {INGEST_TABLE} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_path TEXT UNIQUE,
            file_hash TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


# ---------------------------
# UTILS
# ---------------------------

def file_hash(path):
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


def is_already_ingested(path):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        f"SELECT file_hash FROM {INGEST_TABLE} WHERE file_path = ?",
        (path,)
    )

    row = cur.fetchone()
    conn.close()

    if not row:
        return False

    return row[0] == file_hash(path)


def mark_as_ingested(path):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        f"""
        INSERT OR REPLACE INTO {INGEST_TABLE} (file_path, file_hash)
        VALUES (?, ?)
        """,
        (path, file_hash(path))
    )

    conn.commit()
    conn.close()


# ---------------------------
# PDF PROCESSING
# ---------------------------

def extract_text_from_pdf(path):
    reader = PdfReader(path)
    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    return text


def chunk_text(text, chunk_size=500, overlap=100):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap

    return chunks


# ---------------------------
# EMBEDDING + STORAGE
# ---------------------------

def embed_text(text):
    return get_embeddings(text)  # from Ollama


def store_chunks(chunks, metadata):
    embeddings = [embed_text(c) for c in chunks]

    vector_store.add(
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadata
    )


# ---------------------------
# MAIN INGESTION FUNCTIONS
# ---------------------------

def load_single_pdf(file_path):
    print(f"[INGESTION STARTED] {file_path}")

    if is_already_ingested(file_path):
        print("[SKIPPED] Already ingested:", file_path)
        return

    text = extract_text_from_pdf(file_path)

    if not text.strip():
        print("[WARNING] Empty PDF:", file_path)
        return

    chunks = chunk_text(text)

    metadata = [
        {"source": file_path} for _ in chunks
    ]

    store_chunks(chunks, metadata)

    mark_as_ingested(file_path)

    print(f"[INGESTION COMPLETE] {file_path} | chunks: {len(chunks)}")


# ---------------------------
# INITIAL LOAD (OPTIONAL BOOTSTRAP)
# ---------------------------

def load_all_pdfs(folder="app/knowledge"):
    for file in os.listdir(folder):
        if file.endswith(".pdf"):
            load_single_pdf(os.path.join(folder, file))




class DocumentLoader:

    def load_documents(self, folder="app/knowledge"):

        documents = []

        for file in os.listdir(folder):

            if file.endswith(".pdf"):

                path = os.path.join(
                    folder,
                    file
                )

                text = extract_text_from_pdf(
                    path
                )

                documents.append(
                    {
                        "source": path,
                        "content": text
                    }
                )


        return documents