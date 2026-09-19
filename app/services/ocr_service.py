import pytesseract
import cv2

from app.services.image_preprocessor import ImagePreprocessor


class OCRService:

    def __init__(self):

        print("[OCR SERVICE READY]")
        self.preprocessor = ImagePreprocessor()

    # =========================
    # OCR ONLY FOR TEXT IMAGES
    # =========================
    def extract_text(self, image_path: str):

        image = self.preprocessor.enhance_for_ocr(image_path)

        if image is None:
            return ""

        # grayscale helps OCR accuracy
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        config = r'--oem 3 --psm 6'

        text = pytesseract.image_to_string(gray, config=config)

        return text.strip()