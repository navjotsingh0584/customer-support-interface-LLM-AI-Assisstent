from app.services.ollama_provider import OllamaProvider


class LLMService:

    def __init__(self):
        self.provider = OllamaProvider()

    def generate(
        self,
        prompt: str
    ):
        return self.provider.generate(
            prompt
        )

    def stream_generate(
        self,
        prompt: str
    ):
        return self.provider.stream_generate(
            prompt
        )