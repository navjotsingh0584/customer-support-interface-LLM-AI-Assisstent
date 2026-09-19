from app.services.vision_service import VisionService
from app.services.ocr_service import OCRService



class ImageRouter:


    def __init__(self):

        self.vision = VisionService()
        self.ocr = OCRService()

        print("[IMAGE ROUTER READY]")



    # =========================
    # MAIN ENTRY POINT
    # =========================

    def process(
        self,
        image_path: str
    ):


        # STEP 1:
        # CLASSIFY IMAGE

        image_type = self.vision.classify(
            image_path
        )


        print(
            f"[IMAGE TYPE DETECTED]: {image_type}"
        )



        # =========================
        # VISION BASED IMAGES
        # =========================

        vision_types = [

            "graph",

            "technical_chart",

            "aviation_chart",

            "pie_chart",

            "bar_chart",

            "flowchart",

            "engineering_diagram",

            "circuit_diagram",

            "cad_drawing"

        ]



        if image_type in vision_types:



            result = self.vision.analyze_image(

                image_path,

                image_type      # <-- IMPORTANT FIX

            )



            print(
                "[VISION ANALYSIS COMPLETED]"
            )



            return {


                "source":"vision",


                "type":result.get(

                    "type",

                    image_type

                ),


                "analysis":result.get(

                    "analysis",

                    "No analysis generated"

                )

            }





        # =========================
        # OCR PATH
        # =========================


        text = self.ocr.extract_text(

            image_path

        )



        return {


            "source":"ocr",


            "type":"text_image",


            "analysis":text

        }