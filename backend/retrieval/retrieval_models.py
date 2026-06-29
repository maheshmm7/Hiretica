from typing import List, Optional

from pydantic import BaseModel, Field


class RetrievedCandidate(BaseModel):
    candidate_id: str
    faiss_score: float = 0.0
    bm25_score: float = 0.0
    normalized_faiss_score: float = 0.0
    normalized_bm25_score: float = 0.0
    hybrid_score: float = 0.0
    matched_keywords: List[str] = Field(default_factory=list)
    semantic_similarity: float = 0.0
    retrieval_rank: int = -1
    retrieval_source: str = "hybrid"


class QueryContext(BaseModel):
    job_id: str
    semantic_embedding: Optional[List[float]] = None
    lexical_query: List[str] = Field(default_factory=list)
    raw_text: str = ""
