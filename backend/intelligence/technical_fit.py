from typing import Any, Dict, List, Tuple

from retrieval.retrieval_models import RetrievedCandidate


class TechnicalFitAnalyzer:
    def __init__(
        self,
        semantic_weight: float = 0.5,
        keyword_weight: float = 0.3,
        db_weight: float = 0.2,
    ):
        self.semantic_weight = semantic_weight
        self.keyword_weight = keyword_weight
        self.db_weight = db_weight

    def analyze(
        self, retrieved: RetrievedCandidate, features: Dict[str, Any]
    ) -> Tuple[float, List[Dict[str, Any]]]:
        evidence = []

        # 1. Semantic Match (From FAISS hybrid baseline)
        semantic_score = min(max(retrieved.normalized_faiss_score, 0.0), 1.0)
        evidence.append(
            {
                "dimension": "technical_fit",
                "metric": "semantic_similarity",
                "value": semantic_score,
                "reason": "Excellent contextual alignment with the job requirements." if semantic_score >= 0.7 else "Moderate contextual alignment with the job requirements.",
            }
        )

        # 2. Keyword Match (From core_skill_match_count or BM25)
        bm25_score = min(max(retrieved.normalized_bm25_score, 0.0), 1.0)

        # Check if they have specific vector DB experience (boolean heuristic from features)
        vector_db_exp = features.get("vector_db_experience", False)
        if isinstance(vector_db_exp, str):
            vector_db_exp = vector_db_exp.lower() == "true"

        db_score = 1.0 if vector_db_exp else 0.0

        evidence.append(
            {
                "dimension": "technical_fit",
                "metric": "keyword_match",
                "value": bm25_score,
                "reason": "Strong alignment with the required skills and technologies.",
            }
        )

        if vector_db_exp:
            evidence.append(
                {
                    "dimension": "technical_fit",
                    "metric": "vector_database_experience",
                    "value": db_score,
                    "reason": "Candidate demonstrates relevant hands-on experience in the required technology stack.",
                }
            )

        technical_fit = (
            (semantic_score * self.semantic_weight)
            + (bm25_score * self.keyword_weight)
            + (db_score * self.db_weight)
        )

        return technical_fit, evidence
