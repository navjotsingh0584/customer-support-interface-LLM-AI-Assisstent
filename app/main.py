from app.services.rag_service import RAGService


rag_service = RAGService()
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.auth import router as auth_router
from app.routes.chat import router as chat_router
from app.routes.session import router as session_router
from app.routes.vision import router as vision_router
from app.routes.session import router as session_router
app = FastAPI(
    title="Support Bot API"
)
from fastapi.staticfiles import StaticFiles

app.mount(
    "/uploads",
    StaticFiles(directory="app/uploads"),
    name="uploads"
)
from dotenv import load_dotenv

load_dotenv()
import threading
from app.services.file_watcher import start_watcher
from app.services.document_loader import init_ingestion_db, load_all_pdfs
from app.routes.upload import router as upload_router
@app.on_event("startup")

def startup_event():
    print("[SYSTEM STARTING] Initializing ingestion system...")
    rag_service.load()
    init_ingestion_db()

    # Optional: load existing PDFs once
    load_all_pdfs()

    # Start watcher thread
    thread = threading.Thread(target=start_watcher, daemon=True)
    thread.start()

    print("[SYSTEM READY] RAG + Watcher active")

# CORS
app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],

    allow_credentials=True,

    allow_methods=[
        "*"
    ],

    allow_headers=[
        "*"
    ],
)



# Routes

# Authentication
app.include_router(
    auth_router,
    tags=["Authentication"]
)

app.include_router(session_router)

# Chat + streaming
app.include_router(
    chat_router,
    tags=["Chat"]
)
app.include_router(
    upload_router
)
app.include_router(
    vision_router
)

# Sessions / history
app.include_router(
    session_router,
    prefix="/api",
    tags=["Sessions"]
)



@app.get("/")
def root():

    return {
        "status":"running",
        "service":"HAL Support Bot API"
    }