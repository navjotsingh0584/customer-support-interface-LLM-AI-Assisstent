import fitz  # PyMuPDF
from pathlib import Path

from app.services.image_extractor import ImageExtractor
from app.services.vision_service import VisionService
from app.services.rag_service import RAGService


class PDFProcessor:

    def __init__(self):

        self.image_extractor = ImageExtractor()
        self.vision = VisionService()
        self.rag = RAGService()

        print("[PDF PROCESSOR READY]")


    # =========================
    # MAIN ENTRY
    # =========================
    def process(self, pdf_path: str):

        doc = fitz.open(pdf_path)

        image_dir = Path("app/uploads/pdf_images") / Path(pdf_path).stem

        images = self.image_extractor.extract_images(
            pdf_path,
            str(image_dir)
        )

        images_by_page = self._group_by_page(images)

        final_output = []

        # =========================
        # PAGE LOOP
        # =========================
        for page_number in range(len(doc)):

            page = doc[page_number]
            page_text = page.get_text("text")

            page_images = images_by_page.get(page_number + 1, [])

            # extract structured blocks (for bbox logic)
            blocks = page.get_text("blocks")

            for img in page_images:

                image_path = img["path"]

                # -------------------------
                # Vision Analysis
                # -------------------------
                result = self.vision.analyze_image(image_path)

                image_type = result["type"]
                analysis = result["analysis"]

                # -------------------------
                # Find nearest text context
                # -------------------------
                nearby_text = self._find_nearby_text(blocks)

                # -------------------------
                # Build unified object
                # -------------------------
                document = self._build_multimodal_chunk(
                    page_number + 1,
                    image_path,
                    image_type,
                    analysis,
                    nearby_text
                )

                # -------------------------
                # Store in RAG
                # -------------------------
                self.rag.add_text(
                    text=document,
                    source=pdf_path,
                    doc_type="pdf_image_block",
                    metadata={
                        "page": page_number + 1,
                        "type": image_type
                    }
                )

                final_output.append(document)

            # ALSO store plain page text
            self.rag.add_text(
                text=f"""
PAGE {page_number + 1}

TEXT:
{page_text}
""",
                source=pdf_path,
                doc_type="pdf_text",
                metadata={
                    "page": page_number + 1
                }
            )

        return "\n\n".join(final_output)


    # =========================
    # GROUP IMAGES BY PAGE
    # =========================
    def _group_by_page(self, images):

        grouped = {}

        for img in images:
            grouped.setdefault(img["page"], []).append(img)

        return grouped


    # =========================
    # FIND NEARBY TEXT (BBOX APPROX)
    # =========================
    def _find_nearby_text(self, blocks):

        nearby = []

        for b in blocks:

            # block format: (x0, y0, x1, y1, text, block_no, ...)
            if len(b) >= 5:

                text = b[4].strip()

                if len(text) > 20:  # ignore noise
                    nearby.append(text)

        # return top relevant context
        return "\n".join(nearby[:3])


    # =========================
    # BUILD FINAL MULTIMODAL CHUNK
    # =========================
    def _build_multimodal_chunk(
        self,
        page,
        image_path,
        image_type,
        analysis,
        nearby_text
    ):

        return f"""
========================
MULTIMODAL BLOCK
========================

PAGE: {page}
IMAGE: {image_path}

TYPE: {image_type}

IMAGE ANALYSIS:
{analysis}

RELATED TEXT:
{nearby_text}

NOTE:
This image is semantically linked to the surrounding paragraph.
Use both image + text for answering questions.
""".strip()