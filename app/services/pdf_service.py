import fitz
from pathlib import Path


class PDFService:

    def __init__(self):

        self.image_dir = Path("app/extracted_images")
        self.image_dir.mkdir(exist_ok=True)

    def extract(self, pdf_path):

        document = fitz.open(pdf_path)

        pages = []

        for page_number, page in enumerate(document):

            text = page.get_text()

            page_data = {

                "page": page_number + 1,
                "text": text,
                "images": []

            }

            images = page.get_images(full=True)

            for image_index, image in enumerate(images):

                xref = image[0]

                pix = fitz.Pixmap(document, xref)

                filename = (
                    f"page_{page_number+1}_img_{image_index}.png"
                )

                filepath = self.image_dir / filename

                if pix.alpha:

                    pix = fitz.Pixmap(fitz.csRGB, pix)

                pix.save(filepath)

                page_data["images"].append({

                    "path": str(filepath),
                    "xref": xref

                })

            pages.append(page_data)

        return pages