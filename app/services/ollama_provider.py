import json
import requests



OLLAMA_URL = "http://localhost:11434/api/embeddings"





class OllamaProvider:


    def __init__(
        self,
        chat_model="llama3.1",
        vision_model="llava",
        base_url="http://localhost:11434"
    ):


        self.chat_model = chat_model

        self.vision_model = vision_model

        self.base_url = base_url







    def generate(
        self,
        prompt:str
    ):


        system_prompt = """

You are HAL, an aviation customer support assistant.

Rules:

- Use only provided knowledge.
- Do not invent information.
- Answer using Markdown.
- Use bullet points.
- Use numbered steps for procedures.
- Avoid long paragraphs.

"""


        final_prompt = (
            system_prompt
            +
            "\n\n"
            +
            prompt
        )



        response = requests.post(

            f"{self.base_url}/api/generate",

            json={

                "model":
                self.chat_model,

                "prompt":
                final_prompt,

                "stream":
                False

            }

        )



        if response.status_code != 200:
            print("\n========== OLLAMA ERROR ==========")
            print("Status:", response.status_code)
            print("Response:")
            print(response.text)
            print("==================================\n")
            raise Exception(response.text)

        print(response.json())

        return response.json()["response"]







    def stream_generate(
        self,
        prompt:str
    ):


        response = requests.post(


            f"{self.base_url}/api/generate",


            json={


                "model":
                self.chat_model,


                "prompt":
                prompt,


                "stream":
                True


            },


            stream=True


        )



        response.raise_for_status()





        for line in response.iter_lines():


            if not line:

                continue



            try:


                data = json.loads(
                    line.decode("utf-8")
                )



                if data.get("done"):

                    break



                token = data.get(
                    "response",
                    ""
                )



                if token:

                    yield token



            except Exception as e:


                print(
                    "STREAM ERROR:",
                    e
                )









    def analyze_image(
        self,
        image_path,
        prompt
    ):


        """
        Future vision support
        """



        response = requests.post(


            f"{self.base_url}/api/generate",


            json={


                "model":
                self.vision_model,


                "prompt":
                prompt,


                "images":[
                    image_path
                ],


                "stream":
                False


            }

        )



        response.raise_for_status()



        return response.json()["response"]










def get_embeddings(
    text:str
):


    response = requests.post(

        OLLAMA_URL,

        json={

            "model":
            "nomic-embed-text",

            "prompt":
            text

        }

    )



    response.raise_for_status()



    return response.json()["embedding"]










import re


def clean_markdown(text):


    if not text:

        return text



    text = text.replace(
        "•",
        "-"
    )


    text = re.sub(
        r"(\d+\.)",
        r"\n\1",
        text
    )


    text = re.sub(
        r"(- )",
        r"\n- ",
        text
    )


    return text.strip()