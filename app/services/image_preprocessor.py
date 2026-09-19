import cv2


class ImagePreprocessor:

    def __init__(self):
        print("[IMAGE PREPROCESSOR READY]")

    def enhance_for_ocr(self, image_path: str):

        image = cv2.imread(image_path)

        if image is None:
            return None

        # upscale
        image = cv2.resize(
            image,
            None,
            fx=3,
            fy=3,
            interpolation=cv2.INTER_CUBIC
        )

        # grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # contrast
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        gray = clahe.apply(gray)

        # noise removal
        gray = cv2.GaussianBlur(gray, (3, 3), 0)

        # threshold
        gray = cv2.adaptiveThreshold(
            gray,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            31,
            10
        )

        return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)