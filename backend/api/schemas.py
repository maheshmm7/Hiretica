from typing import Dict, List, Any

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


class WorkspaceCandidate(BaseModel):
    candidate_id: str
    overall_rank: int
    final_score: float
    
    hybrid_score: float
    recruiter_score: float
    behavior_score: float
    
    ranking_breakdown: Dict[str, float]
    evidence_summary: List[Any]
    
    reasoning: str
    positive_factors: List[str]
    negative_factors: List[str]


class DashboardMetrics(BaseModel):
    total_candidates: int
    avg_score: float
    avg_hybrid: float
    avg_recruiter: float
    avg_behavior: float


class ChartData(BaseModel):
    recruiter_distribution: Dict[str, int]
    behavior_distribution: Dict[str, int]


class WorkspaceResponse(BaseModel):
    job_summary: Dict[str, Any]
    pipeline_metrics: Dict[str, Any]
    dashboard_metrics: DashboardMetrics
    chart_data: ChartData
    candidates: List[WorkspaceCandidate]
    submission_preview: List[SubmissionCandidate]
