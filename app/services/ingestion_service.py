from pathlib import Path

from app.services.pdf_processor import PDFProcessor
from app.services.image_processor import ImageProcessor
from app.services.table_processor import TableProcessor


class IngestionService:

    def __init__(self):

        # =========================
        # CORE PROCESSORS
        # =========================
        self.pdf = PDFProcessor()
        self.image = ImageProcessor()
        self.table = TableProcessor()

        print("[INGESTION SERVICE READY]")


    # =========================
    # FILE TYPE MAPS
    # =========================
    IMAGE_EXTENSIONS = {
        ".png", ".jpg", ".jpeg", ".bmp",
        ".tiff", ".webp", ".avif", ".heic"
    }

    TABLE_EXTENSIONS = {
        ".csv", ".xlsx"
    }


    # =========================
    # MAIN ENTRY POINT
    # =========================
    def ingest(self, file_path: str):

        ext = Path(file_path).suffix.lower()

        # -------------------------
        # PDF PIPELINE
        # -------------------------
        if ext == ".pdf":

            print("[INGEST] PDF")

            return self.pdf.process(file_path)


        # -------------------------
        # IMAGE / GRAPH / DIAGRAM
        # -------------------------
        if ext in self.IMAGE_EXTENSIONS:

            print("[INGEST] IMAGE")

            return self.image.process(file_path)


        # -------------------------
        # TABLE PIPELINE
        # -------------------------
        if ext in self.TABLE_EXTENSIONS:

            print("[INGEST] TABLE")

            return self.table.process(file_path)


        # -------------------------
        # UNSUPPORTED FILE
        # -------------------------
        raise ValueError(f"Unsupported file type: {ext}")