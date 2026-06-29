from typing import Dict, List

from pydantic import BaseModel, Field

from ensemble.ensemble_models import RankedCandidate, SubmissionCandidate
from explainability.explanation_models import ExplainedCandidate


class RankRequest(BaseModel):
    job_id: str = Field(..., description="Unique identifier for the job")
    job_description: str = Field(
        ..., min_length=10, description="Full text of the job description"
    )


class ExplainRequest(BaseModel):
    candidates: List[RankedCandidate] = Field(
        ..., description="A list of RankedCandidate objects to explain"
    )


class RankResponse(BaseModel):
    job_id: str
    candidates: List[SubmissionCandidate]


class ExplainResponse(BaseModel):
    candidates: List[ExplainedCandidate]


class HealthResponse(BaseModel):
    status: str
    version: str
    components: Dict[str, str]


class MetricsResponse(BaseModel):
    startup_time_ms: float
    is_ready: bool
