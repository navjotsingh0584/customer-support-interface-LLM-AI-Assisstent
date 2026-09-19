import chromadb
import requests


class VectorStore:

    def __init__(self):

        print("VECTOR INIT")

        self.client = chromadb.PersistentClient(
            path="chroma_db"
        )

        self.collection = self.client.get_or_create_collection(
            name="support_docs"
        )

        print("VECTOR READY")

    # =========================
    # EMBEDDINGS
    # =========================
    def create_embedding(self, text: str):

        response = requests.post(
            "http://localhost:11434/api/embeddings",
            json={
                "model": "nomic-embed-text",
                "prompt": text
            },
            timeout=60
        )

        response.raise_for_status()

        return response.json()["embedding"]

    # =========================
    # ADD DOCUMENTS
    # =========================
    def add(self, documents, embeddings=None, metadatas=None):

        print("VECTOR ADD START")

        if not documents:
            print("NO DOCUMENTS TO ADD")
            return

        if embeddings is None:
            embeddings = [
                self.create_embedding(doc)
                for doc in documents
            ]

        start_id = self.collection.count()

        ids = [
            str(start_id + i)
            for i in range(len(documents))
        ]

        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
        )

        print("ADDED CHUNKS:", len(documents))

    # =========================
    # KEYWORD SCORING
    # =========================
    def _keyword_score(self, query, text):

        if not text:
            return 0

        q = set(query.lower().split())
        t = set(text.lower().split())

        return len(q.intersection(t)) * 0.1

    # =========================
    # SEARCH (SESSION-AWARE + HYBRID RERANKING)
    # =========================
    def search(self, query, where=None):

        print("SEARCH START")

        embedding = self.create_embedding(query)

        query_params = {
            "query_embeddings": [embedding],
            "n_results": 8,
            "include": ["documents", "metadatas", "distances"]
        }

        # 🔥 SESSION / FILTER SUPPORT
        if where:
            query_params["where"] = where

        result = self.collection.query(**query_params)

        if not result:
            return {"context": "", "sources": []}

        documents = result.get("documents", [[]])[0]
        metadatas = result.get("metadatas", [[]])[0]
        distances = result.get("distances", [[]])[0]

        if not documents:
            return {"context": "", "sources": []}

        scored = []

        for doc, meta, dist in zip(documents, metadatas, distances):

            vector_score = 1 - dist
            keyword_score = self._keyword_score(query, doc)

            # =========================
            # METADATA BOOSTING
            # =========================
            meta_score = 0

            if meta:
                doc_type = meta.get("type")

                if doc_type == "table":
                    meta_score += 0.25
                elif doc_type == "image":
                    meta_score += 0.20
                elif doc_type == "pdf":
                    meta_score += 0.30
                elif doc_type == "text":
                    meta_score += 0.10

            final_score = vector_score + keyword_score + meta_score

            scored.append((final_score, doc, meta))

        # sort best matches first
        scored.sort(reverse=True, key=lambda x: x[0])

        top_docs = []
        sources = []

        for score, doc, meta in scored[:4]:

            top_docs.append(doc)

            if meta:
                src = meta.get("source")
                if src and src not in sources:
                    sources.append(src)

        context = "\n\n".join(top_docs)
        context = context.replace(" | ", " ")

        print("SEARCH DONE")

        return {
            "context": context,
            "sources": sources
        }

    # =========================
    # UTIL: CHECK EMPTY DB
    # =========================
    def is_empty(self):

        return self.collection.count() == 0

    # =========================
    # UTIL: CLEAR DB
    # =========================
    def clear(self):

        print("CLEARING VECTOR STORE")

        try:
            self.client.delete_collection("support_docs")
        except Exception:
            pass

        self.collection = self.client.get_or_create_collection(
            name="support_docs"
        )

        print("VECTOR STORE CLEARED")

    # =========================
    # UTIL: GET ALL SOURCES
    # =========================
    def get_sources(self):

        result = self.collection.get(include=["metadatas"])

        sources = []

        for meta in result.get("metadatas", []):

            if meta:
                src = meta.get("source")

                if src and src not in sources:
                    sources.append(src)

        return sources