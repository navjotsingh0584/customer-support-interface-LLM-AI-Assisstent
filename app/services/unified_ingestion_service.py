from pathlib import Path

from app.services.pdf_processor import PDFProcessor
from app.services.vision_service import VisionService
from app.services.rag_service import RAGService


class UnifiedIngestionService:

    def __init__(self):

        self.pdf = PDFProcessor()
        self.vision = VisionService()
        self.rag = RAGService()


    # =========================
    # MAIN ENTRY POINT
    # =========================
    def ingest(self, file_path: str):

        ext = Path(file_path).suffix.lower()

        # -------------------------
        # PDF
        # -------------------------
        if ext == ".pdf":

            return self.pdf.process(file_path)

        # -------------------------
        # IMAGE / GRAPH / CHART
        # -------------------------
        elif ext in [".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tiff"]:

            return self._process_image(file_path)

        else:

            return "Unsupported file type"


    # =========================
    # IMAGE / GRAPH PROCESSING
    # =========================
    def _process_image(self, file_path: str):

        result = self.vision.analyze_image(file_path)

        image_type = result["type"]
        analysis = result["analysis"]

        # store in RAG
        self.rag.add_text(
            text=f"""
IMAGE UPLOAD

TYPE: {image_type}

ANALYSIS:
{analysis}

USAGE:
This data can be used for answering questions, summarization, and reasoning.
""",
            source=file_path
        )

        return {
            "type": image_type,
            "analysis": analysis
        }