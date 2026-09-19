import fitz
import os


class ImageExtractor:

    def extract_images(self, pdf_path, output_folder):

        doc = fitz.open(pdf_path)

        os.makedirs(output_folder, exist_ok=True)

        images = []

        for page_index in range(len(doc)):

            page = doc[page_index]

            image_list = page.get_images(full=True)

            for img_index, img in enumerate(image_list):

                xref = img[0]

                base_image = doc.extract_image(xref)

                image_bytes = base_image["image"]
                img_ext = base_image["ext"]

                image_path = os.path.join(
                    output_folder,
                    f"page_{page_index+1}_img_{img_index}.{img_ext}"
                )

                with open(image_path, "wb") as f:
                    f.write(image_bytes)

                rects = page.get_image_rects(xref)

                bbox = None
                if rects:
                    r = rects[0]
                    bbox = (r.x0, r.y0, r.x1, r.y1)

                images.append({
                    "path": image_path,
                    "page": page_index + 1,
                    "bbox": bbox,
                    "xref": xref
                })

        return images