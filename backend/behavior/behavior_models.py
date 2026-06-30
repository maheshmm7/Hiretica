from typing import Dict, List

from pydantic import BaseModel, ConfigDict, Field


class BehaviorEvidence(BaseModel):
    module: str
    reason: str
    impact: float


class BehaviorCandidate(BaseModel):
    # Core reference
    candidate_id: str

    # Previous phase scores
    recruiter_score: float
    recruiter_risk_multiplier: float

    # Behavioral sub-scores
    availability_score: float = 0.0
    engagement_score: float = 0.0
    profile_quality_score: float = 0.0

    # Final behavior scores
    behavior_score: float = 0.0
    behavior_confidence: float = 0.0
    hiring_readiness: str = "Unlikely"  # Highly Ready, Ready, Passive, Unlikely

    # Diagnostics
    behavior_breakdown: Dict[str, float] = Field(default_factory=dict)
    recruiter_evidence: List[BehaviorEvidence] = Field(default_factory=list)
    behavior_evidence: List[BehaviorEvidence] = Field(default_factory=list)
    behavior_flags: List[str] = Field(default_factory=list)

    # Embedded original RecruiterCandidate (optional, or just inherit id)
    # The instructions say: "Include: candidate_id, recruiter_score, behavior_score..."
    # Keep it flat for easier API transport later.
    model_config = ConfigDict(frozen=True)
