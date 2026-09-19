from app.services.vector_store import VectorStore
from app.services.session_store import SessionStore
import re


class RAGService:

    def __init__(self):
        print("RAG INIT")

        self.store = VectorStore()
        self.session_store = SessionStore()

        self.loaded = False

    # =========================
    # ADD TEXT (UNCHANGED CORE LOGIC)
    # =========================
    def add_text(
    self,
    text,
    source="uploaded_file",
    doc_type="text",
    metadata=None
):

        if not text:
            return


        chunks = self.split_text(text)


        metadatas = []


        for _ in chunks:

            meta = {
                "source": source,
                "type": doc_type
            }


            if metadata:
                meta.update(metadata)


            metadatas.append(meta)



        self.store.add(
            documents=chunks,
            metadatas=metadatas
        )


        print(
            f"RAG ADDED: {source} | chunks={len(chunks)} | metadata={metadata}"
        )

    # =========================
    # CHUNKING (UNCHANGED)
    # =========================
    def split_text(self, text, chunk_size=900):

        text = re.sub(r'\n+', '\n', text)
        paragraphs = text.split("\n")

        chunks = []
        current = ""

        for p in paragraphs:
            p = p.strip()
            if not p:
                continue

            if len(current) + len(p) > chunk_size:
                chunks.append(current.strip())
                current = p + "\n"
            else:
                current += p + "\n"

        if current.strip():
            chunks.append(current.strip())

        return chunks

    # =========================
    # 🔥 STEP 3: MULTI-DOCUMENT CONTEXT BUILDER
    # =========================
    def build_document_context(self, session_id):

        files = self.session_store.get_uploaded_files(session_id)

        if not files:
            return ""

        context = ""

        for f in files:

            context += f"""
Filename: {f['filename']}
Type: {f['file_type']}
Uploaded: {f['created_at']}

Content:
{f['content']}

-------------------------------
"""

        return context

    # =========================
    # RETRIEVAL (UPDATED FOR MULTI-DOC)
    # =========================
    def get_context(self, question, session_id=None):

        self.load()

        # 1. Build full document context
        document_context = ""

        if session_id:
            document_context = self.build_document_context(session_id)

        # DEBUG
        print("\n[ACTIVE DOCUMENTS CONTEXT]\n", document_context[:500])

        # 2. Combine query + document context (IMPORTANT IMPROVEMENT)
        enhanced_query = question

        if document_context:
            enhanced_query = f"""
User Question:
{question}

Available Documents:
{document_context[:1500]}

Task:
Use the documents above to answer the question accurately.
Focus on charts, tables, and structured data when present.
"""

        print("\n[ENHANCED QUERY]\n", enhanced_query)

        # 3. Vector search (unchanged)
        result = self.store.search(
            query=enhanced_query,
            where={"session_id": session_id} if session_id else None
        )
        print(
    "SEARCH FILTER:",
    {
        "session_id": session_id
    }
)
        if not result:
            return {
                "context": "",
                "sources": []
            }

        return {
            "context": result["context"],
            "sources": result["sources"]
        }

    # =========================
    # LOAD
    # =========================
    def load(self):

        if self.loaded:
            return

        print("RAG LOAD START")
        self.loaded = True