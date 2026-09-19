from app.services.vector_store import VectorStore
from app.services.rag_service import RAGService


print("STARTING REBUILD")


store = VectorStore()

store.clear()


rag = RAGService()

rag.load()


print("REBUILD COMPLETE")