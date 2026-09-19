import base64
import tempfile

import requests
from PIL import Image, ImageEnhance, ImageFilter



class VisionService:


    def __init__(
        self,
        model="llava",
        base_url="http://localhost:11434"
    ):

        self.model = model
        self.base_url = base_url



    # =====================================
    # IMAGE PREPROCESS
    # =====================================

    def _prepare_image(
        self,
        image_path:str
    ):


        image = Image.open(
            image_path
        )


        if image.mode != "RGB":

            image = image.convert(
                "RGB"
            )


        # upscale
        image = image.resize(
            (
                image.width * 8,
                image.height * 8
            )
        )
 
        image = ImageEnhance.Contrast(
            image
        ).enhance(2)


        image = ImageEnhance.Sharpness(
            image
        ).enhance(3)


        image = image.filter(
            ImageFilter.SHARPEN
)
        

        temp = tempfile.NamedTemporaryFile(
            suffix=".png",
            delete=False
        )


        image.save(
            temp.name,
            "PNG"
        )


        return temp.name

        # =====================================
    # LLAVA CALL
    # =====================================

    def _call(
        self,
        image_path:str,
        prompt:str
    ):


        image_path = self._prepare_image(
            image_path
        )


        with open(
            image_path,
            "rb"
        ) as f:

            image = base64.b64encode(
                f.read()
            ).decode()



        response = requests.post(

            f"{self.base_url}/api/chat",

            json={

                "model": self.model,


                "messages":[

                    {

                        "role":"user",

                        "content":prompt,

                        "images":[image]

                    }

                ],


                # Vision accuracy control
                "options":{

                    # Less hallucination
                    "temperature":0.1,


                    # More context for graph reading
                    "num_ctx":4096

                },


                "stream":False

            }

        )


        response.raise_for_status()


        result = response.json()


        return result["message"]["content"]


    




    # =====================================
    # CLASSIFY IMAGE
    # =====================================

    def classify(
        self,
        image_path:str
    ):


        prompt = """

Classify this image.

Return ONLY one label.


Labels:

graph
aviation_chart
technical_chart
engineering_diagram
cad_drawing
flowchart
circuit_diagram
document
photo
unknown



Priority rules:


1. GRAPH

Choose graph if image contains:

- x axis
- y axis
- curves
- plotted lines
- grid
- numbers
- legends



2. AVIATION_CHART

Choose aviation_chart if visible:

- aircraft
- lift coefficient
- drag coefficient
- angle of attack
- stall
- airspeed



3. ENGINEERING_DIAGRAM

Choose engineering_diagram if:

- turbine
- engine
- blade
- nozzle
- shaft
- machine components



4. DOCUMENT

Mostly text page.



5. PHOTO

Real world photograph.



Return only label.

"""


        result = self._call(
            image_path,
            prompt
        )


        result = result.lower().strip()


        labels=[

            "aviation_chart",
            "engineering_diagram",
            "technical_chart",
            "graph",
            "cad_drawing",
            "flowchart",
            "circuit_diagram",
            "document",
            "photo"

        ]


        for label in labels:

            if label in result:

                return label



        return "unknown"





    # =====================================
    # ANALYZE IMAGE
    # =====================================

    def analyze_image(
        self,
        image_path:str,
        image_type:str="unknown"
    ):


        print(
            "VISION TYPE USED:",
            image_type
        )



        prompts={


"graph":"""

You are analyzing a high resolution scientific graph.

IMPORTANT:
Before answering, inspect the image carefully.

You MUST attempt to read:

- graph title
- x-axis label
- y-axis label
- units
- tick values
- curve labels
- annotations


Do not immediately say unclear.

If text is partially readable, provide the closest readable text.

Return:


📊 Graph Analysis


Title:
-


X Axis:
- Label:
- Unit:
- Visible tick values:


Y Axis:
- Label:
- Unit:
- Visible tick values:


Numeric Data:
- List every number visible in the graph.


Curve Information:
-


Trend:
-


Engineering Explanation:
-


Confidence:
-


Rules:

- Never invent numbers.
- Never use external knowledge.
- Try OCR style reading first.

""",



"technical_chart":"""

Analyze this technical chart.


Return:


📈 Technical Chart Analysis


Title:

Axes:

Units:

Curves:

Trend:

Engineering Meaning:


Do not guess values.

""",



"engineering_diagram":"""

Analyze this engineering diagram.


Return:


⚙️ Engineering Diagram Analysis


System:

Components:

Connections:

Working Principle:

Application:


Use visible labels only.

Do not hallucinate.

""",



"cad_drawing":"""

Analyze CAD drawing.

Return:

Parts:

Dimensions visible:

Structure:

Do not guess.

""",



"flowchart":"""

Analyze flowchart.

Return:

Steps:

Decisions:

Connections:

Process:

""",



"circuit_diagram":"""

Analyze circuit diagram.

Return:

Components:

Connections:

Signal flow:

""",



"document":"""

Analyze document image.

Extract:

Text:

Headings:

Tables:

Important information:

""",



"photo":"""

Describe visible objects only.

""",



"unknown":"""

Describe only clearly visible information.

Do not guess.

"""

        }



        prompt = prompts.get(
            image_type,
            prompts["unknown"]
        )



        analysis = self._call(

            image_path,

            prompt

        )



        print(
            "VISION OUTPUT:",
            analysis[:500]
        )



        return {

            "source":"vision",

            "type":image_type,

            "analysis":analysis

        }