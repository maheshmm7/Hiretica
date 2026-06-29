from fastapi import APIRouter, Depends, HTTPException

from core.pipeline import AIPipeline

from .dependencies import get_pipeline
from .exceptions import PipelineError
from .schemas import (ExplainRequest, ExplainResponse, HealthResponse,
                      MetricsResponse, RankRequest, RankResponse)

router = APIRouter()
system_router = APIRouter()


@system_router.get("/", tags=["System"])
def read_root():
    return {"message": "HIRETICA API is running."}


@system_router.get("/health", response_model=HealthResponse, tags=["System"])
def health_check(pipeline: AIPipeline = Depends(get_pipeline)):
    return HealthResponse(
        status="ok",
        version="1.0.0",
        components={
            "pipeline": "ready" if pipeline.is_ready else "not_ready",
            "faiss": "ready",
            "bm25": "ready",
        },
    )


@system_router.get("/version", tags=["System"])
def get_version():
    return {"version": "1.0.0"}


@system_router.get("/config", tags=["Configuration"])
def get_config():
    # In a real system, we might return the ranking_config.yaml dict here.
    return {"status": "Config loaded"}


@system_router.get("/metrics", response_model=MetricsResponse, tags=["System"])
def get_metrics(pipeline: AIPipeline = Depends(get_pipeline)):
    return MetricsResponse(
        startup_time_ms=pipeline.startup_time, is_ready=pipeline.is_ready
    )


@router.post("/rank", response_model=RankResponse, tags=["Ranking"])
def rank_candidates(request: RankRequest, pipeline: AIPipeline = Depends(get_pipeline)):
    if not request.job_description.strip():
        raise HTTPException(status_code=400, detail="Job description cannot be empty.")

    try:
        submission = pipeline.run_pipeline(request.job_id, request.job_description)
        return RankResponse(job_id=request.job_id, candidates=submission)
    except Exception as e:
        raise PipelineError(f"Pipeline failed: {str(e)}", status_code=500)


@router.post("/explain", response_model=ExplainResponse, tags=["Explainability"])
def explain_candidates(
    request: ExplainRequest, pipeline: AIPipeline = Depends(get_pipeline)
):
    if not request.candidates:
        raise HTTPException(status_code=400, detail="Candidates list cannot be empty.")

    try:
        explained = pipeline.explain(request.candidates)
        return ExplainResponse(candidates=explained)
    except Exception as e:
        raise PipelineError(f"Explainability failed: {str(e)}", status_code=500)
