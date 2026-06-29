from typing import List

import numpy as np
from sentence_transformers import SentenceTransformer


class EmbeddingService:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def generate_embedding(self, text: str) -> List[float]:
        """
        Generates L2-normalized embedding for the given text.
        """
        embedding = self.model.encode(text, convert_to_numpy=True)
        # L2 Normalization (FAISS IndexFlatIP requires normalized vectors for Cosine Similarity)
        norm = np.linalg.norm(embedding)
        if norm > 0:
            embedding = embedding / norm
        return embedding.tolist()
