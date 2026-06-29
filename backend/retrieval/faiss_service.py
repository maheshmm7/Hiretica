from typing import Dict, List

import faiss
import numpy as np
import pandas as pd


class FaissService:
    def __init__(self, index_path: str, metadata_path: str):
        self.index = faiss.read_index(index_path)
        # Load metadata to map FAISS sequential IDs back to candidate IDs
        # The metadata parquet should be aligned with the FAISS index
        self.metadata = pd.read_parquet(metadata_path)

    def search(self, embedding: List[float], top_n: int) -> Dict[str, float]:
        """
        Searches the FAISS index and returns a mapping of {candidate_id: faiss_score}.
        """
        query_vector = np.array([embedding], dtype=np.float32)
        distances, indices = self.index.search(query_vector, top_n)

        results = {}
        for i, faiss_idx in enumerate(indices[0]):
            if faiss_idx != -1 and faiss_idx < len(self.metadata):
                candidate_id = self.metadata.iloc[faiss_idx]["candidate_id"]
                score = float(distances[0][i])
                results[candidate_id] = score

        return results
