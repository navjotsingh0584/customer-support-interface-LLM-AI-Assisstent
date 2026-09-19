import base64
import requests


class ChartAnalyzer:

    def __init__(self, model="llava", base_url="http://localhost:11434"):
        self.model = model
        self.base_url = base_url

    def analyze(self, image_path: str):

        with open(image_path, "rb") as f:
            img = base64.b64encode(f.read()).decode()

        prompt = """
You are an expert chart analysis system.

Analyze this image carefully.

If it is a pie chart:
- Extract all percentages
- Identify largest and smallest segment
- Count number of slices

Return ONLY JSON:

{
  "type": "",
  "values": [],
  "largest": "",
  "smallest": "",
  "summary": ""
}
"""

        response = requests.post(
            f"{self.base_url}/api/chat",
            json={
                "model": self.model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt,
                        "images": [img]
                    }
                ],
                "stream": False
            }
        )

        return response.json()["message"]["content"]