import numpy as np

class CLIPEmbedder:

    def encode(self, image):
        # Replace with real CLIP later (OpenAI / OpenCLIP)
        return np.random.rand(512)

    def similarity(self, a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))