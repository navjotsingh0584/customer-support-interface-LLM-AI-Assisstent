from pathlib import Path

from app.services.pdf_processor import PDFProcessor
from app.services.vision_service import VisionService
from app.services.table_processor import TableProcessor
from app.services.rag_service import RAGService


class FileProcessor:

    def __init__(self):

        # ======================
        # CORE PROCESSORS
        # ======================
        self.pdf = PDFProcessor()
        self.vision = VisionService()
        self.table = TableProcessor()

        # ======================
        # SINGLE INGESTION LAYER
        # ======================
        self.rag = RAGService()

        print("FILE PROCESSOR READY")

    # ======================
    # IMAGE TYPES
    # ======================
    IMAGE_EXTENSIONS = {
        ".png",
        ".jpg",
        ".jpeg",
        ".bmp",
        ".tiff",
        ".webp",
        ".avif",
        ".heic"
    }

    # ======================
    # TABLE TYPES
    # ======================
    TABLE_EXTENSIONS = {
        ".csv",
        ".xlsx"
    }

    # ======================
    # MAIN PROCESS PIPELINE
    # ======================
    def process(self, path):

        ext = Path(path).suffix.lower()

        # ======================
        # PDF PROCESSING
        # ======================
        if ext == ".pdf":

            print("PROCESSING PDF")

            result = self.pdf.process(path)

            # 🔥 INGEST INTO RAG
            self.rag.add_text(
                text=result,
                source=path
            )

            return result

        # ======================
        # IMAGE PROCESSING
        # ======================
        if ext in self.IMAGE_EXTENSIONS:

            print("PROCESSING IMAGE")

            result = self.vision.analyze_image(path)

            # 🔥 INGEST INTO RAG
            self.rag.add_text(
                text=result,
                source=path
            )

            return result

        # ======================
        # TABLE PROCESSING
        # ======================
        if ext in self.TABLE_EXTENSIONS:

            print("PROCESSING TABLE")

            result = self.table.process(path)

            # 🔥 INGEST INTO RAG
            self.rag.add_text(
                text=result,
                source=path
            )

            return result

        # ======================
        # UNSUPPORTED FILE
        # ======================
        print("UNSUPPORTED FILE TYPE")

        return ""