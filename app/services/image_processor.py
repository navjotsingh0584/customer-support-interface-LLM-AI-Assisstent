from app.services.vision_service import VisionService
from app.services.rag_service import RAGService


class ImageProcessor:

    def __init__(self):

        self.vision = VisionService()
        self.rag = RAGService()

        print("[IMAGE PROCESSOR READY]")


    # =========================
    # MAIN ENTRY POINT
    # =========================
    def process(self, image_path: str):

        # 1. Run vision model (classification + analysis)
        result = self.vision.analyze_image(image_path)

        image_type = result["type"]
        analysis = result["analysis"]

        # 2. Convert to structured document for RAG
        document = self._build_document(
            image_type=image_type,
            analysis=analysis,
            image_path=image_path
        )

        # 3. Store in RAG (IMPORTANT)
        self.rag.add_text(
            text=document,
            source=image_path,
            doc_type=image_type
        )

        # 4. Return structured response (for API/chat UI)
        return {
            "type": image_type,
            "analysis": analysis,
            "status": "ingested"
        }


    # =========================
    # BUILD CLEAN RAG DOCUMENT
    # =========================
    def _build_document(self, image_type, analysis, image_path):

        return f"""
IMAGE INGESTION

SOURCE: {image_path}

TYPE: {image_type}

ANALYSIS:
{analysis}

CONTEXT:
This image is part of a multimodal knowledge base.
It can be used to answer questions, summarize content,
and explain diagrams or charts.
""".strip()