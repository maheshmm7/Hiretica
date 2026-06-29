import pickle
from typing import Dict, List

import pandas as pd


class Bm25Service:
    def __init__(self, index_path: str, metadata_path: str):
        with open(index_path, "rb") as f:
            self.bm25 = pickle.load(f)
        self.metadata = pd.read_parquet(metadata_path)

    def score_candidates(
        self, lexical_query: List[str], candidate_ids: List[str]
    ) -> Dict[str, float]:
        """
        Scores a specific subset of candidates using BM25.
        This assumes we are scoring candidates retrieved by FAISS for fusion,
        or scoring the entire corpus if we do parallel retrieval.
        """
        # In a real heavy-duty scenario we'd query the whole BM25 and get top_n,
        # but the standard rank_bm25 scores the whole corpus anyway.
        doc_scores = self.bm25.get_scores(lexical_query)

        results = {}
        # We need a fast way to map candidate_id to BM25 index.
        # Since metadata ordering aligns with BM25 documents (built from the same parquet)
        # Let's create a map once.
        if not hasattr(self, "_id_to_idx"):
            self._id_to_idx = {
                cid: idx for idx, cid in enumerate(self.metadata["candidate_id"])
            }

        for cid in candidate_ids:
            if cid in self._id_to_idx:
                idx = self._id_to_idx[cid]
                results[cid] = float(doc_scores[idx])

        return results

    def search(self, lexical_query: List[str], top_n: int) -> Dict[str, float]:
        """
        Performs a full BM25 search for the top_n candidates across the entire corpus.
        """
        doc_scores = self.bm25.get_scores(lexical_query)
        # Get indices of top_n scores
        top_indices = sorted(
            range(len(doc_scores)), key=lambda i: doc_scores[i], reverse=True
        )[:top_n]

        results = {}
        for idx in top_indices:
            candidate_id = self.metadata.iloc[idx]["candidate_id"]
            results[candidate_id] = float(doc_scores[idx])

        return results
