from typing import Dict, List

from .retrieval_models import RetrievedCandidate


class HybridRetriever:
    def __init__(self, alpha: float, normalization: str = "minmax"):
        self.alpha = alpha
        self.normalization = normalization

    def _minmax_normalize(self, scores: Dict[str, float]) -> Dict[str, float]:
        if not scores:
            return {}

        vals = list(scores.values())
        min_v = min(vals)
        max_v = max(vals)

        # If all scores are the same, return 1.0
        if max_v == min_v:
            return {k: 1.0 for k in scores}

        return {k: (v - min_v) / (max_v - min_v) for k, v in scores.items()}

    def _zscore_normalize(self, scores: Dict[str, float]) -> Dict[str, float]:
        import statistics

        if not scores:
            return {}

        vals = list(scores.values())
        if len(vals) < 2:
            return {k: 1.0 for k in scores}

        mean_v = statistics.mean(vals)
        stdev_v = statistics.stdev(vals)

        if stdev_v == 0:
            return {k: 1.0 for k in scores}

        # Z-score normalization
        return {k: (v - mean_v) / stdev_v for k, v in scores.items()}

    def normalize(self, scores: Dict[str, float]) -> Dict[str, float]:
        if self.normalization == "minmax":
            return self._minmax_normalize(scores)
        elif self.normalization == "zscore":
            return self._zscore_normalize(scores)
        else:
            return scores

    def fuse(
        self,
        faiss_scores: Dict[str, float],
        bm25_scores: Dict[str, float],
        query_keywords: List[str],
    ) -> List[RetrievedCandidate]:
        """
        Fuses FAISS and BM25 scores. Deduplicates candidates and calculates the final hybrid score.
        """
        norm_faiss = self.normalize(faiss_scores)
        norm_bm25 = self.normalize(bm25_scores)

        candidates_map: Dict[str, RetrievedCandidate] = {}

        # Merge FAISS
        for cid, norm_f in norm_faiss.items():
            f_score = faiss_scores[cid]
            candidates_map[cid] = RetrievedCandidate(
                candidate_id=cid,
                faiss_score=f_score,
                normalized_faiss_score=norm_f,
                semantic_similarity=f_score,  # For IndexFlatIP this is similar to cosine
                retrieval_source="faiss",
            )

        # Merge BM25
        for cid, norm_b in norm_bm25.items():
            b_score = bm25_scores[cid]
            if cid in candidates_map:
                cand = candidates_map[cid]
                cand.bm25_score = b_score
                cand.normalized_bm25_score = norm_b
                cand.retrieval_source = "hybrid"
            else:
                candidates_map[cid] = RetrievedCandidate(
                    candidate_id=cid,
                    bm25_score=b_score,
                    normalized_bm25_score=norm_b,
                    retrieval_source="bm25",
                )

        # Calculate Hybrid Score
        final_candidates = []
        for cand in candidates_map.values():
            cand.hybrid_score = (self.alpha * cand.normalized_faiss_score) + (
                (1 - self.alpha) * cand.normalized_bm25_score
            )
            final_candidates.append(cand)

        # Sort descending
        final_candidates.sort(key=lambda c: c.hybrid_score, reverse=True)

        # Apply rank
        for i, cand in enumerate(final_candidates):
            cand.retrieval_rank = i + 1

        return final_candidates
