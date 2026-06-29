from typing import Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field

from behavior.behavior_models import BehaviorEvidence


class RankedCandidate(BaseModel):
    candidate_id: str

    hybrid_score: float
    recruiter_score: float
    behavior_score: float

    final_hiretica_score: float
    overall_rank: int = 0

    ranking_breakdown: Dict[str, float] = Field(default_factory=dict)
    evidence_summary: List[BehaviorEvidence] = Field(default_factory=list)

    model_config = ConfigDict(frozen=True)


class SubmissionCandidate(BaseModel):
    candidate_id: str
    rank: int
    score: float
    reasoning: Optional[str] = None

    model_config = ConfigDict(frozen=True)
