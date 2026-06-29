from typing import Any, Dict, List

from pydantic import BaseModel, Field


class RecruiterCandidate(BaseModel):
    candidate_id: str

    # Retrieval Baseline (from Hybrid Retriever)
    faiss_score: float = 0.0
    bm25_score: float = 0.0
    hybrid_score: float = 0.0

    # Intelligence Sub-scores (Base 0.0 to 1.0)
    technical_fit: float = 0.0
    experience_fit: float = 0.0
    career_progression: float = 0.0
    leadership_score: float = 0.0
    production_ai_score: float = 0.0
    retrieval_experience: bool = False
    vector_database_experience: bool = False
    evaluation_framework_score: float = 0.0
    domain_relevance: float = 0.0
    career_stability: float = 0.0
    growth_trend: float = 0.0

    # Risk and Confidence
    risk_multiplier: float = 1.0
    recruiter_confidence: float = 0.0
    confidence_band: str = "Low"  # Low, Medium, High, Exceptional

    # Final Output
    base_recruiter_score: float = 0.0
    recruiter_score: float = 0.0

    # Explainability Data
    score_breakdown: Dict[str, float] = Field(default_factory=dict)
    evidence: List[Dict[str, Any]] = Field(default_factory=list)
