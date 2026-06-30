from typing import List

from pydantic import BaseModel, ConfigDict, Field

from ensemble.ensemble_models import RankedCandidate


class ExplanationMetadata(BaseModel):
    template_id: str
    evidence_used: int
    generated_length: int
    generation_time_ms: float

    model_config = ConfigDict(frozen=True)


class ExplainedCandidate(BaseModel):
    candidate_id: str
    rank: int
    score: float

    reasoning: str
    positive_factors: List[str] = Field(default_factory=list)
    negative_factors: List[str] = Field(default_factory=list)
    explanation_metadata: ExplanationMetadata

    ranked_candidate: RankedCandidate

    model_config = ConfigDict(frozen=True)
