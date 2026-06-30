import os
import time
from typing import List

from behavior.behavior_engine import BehaviorIntelligenceEngine
from config.settings import settings
from ensemble.ensemble_engine import FinalEnsembleEngine
from ensemble.ensemble_models import RankedCandidate, SubmissionCandidate
from explainability.explainability_engine import ExplainabilityEngine
from explainability.explanation_models import ExplainedCandidate
from intelligence.recruiter_intelligence import RecruiterIntelligenceEngine
from retrieval.candidate_selector import CandidateSelector


class AIPipeline:
    """
    Singleton orchestrator for the entire AI ranking pipeline.
    Initializes ML models, parsers, and engines exactly once.
    """

    def __init__(self, cache_dir: str):
        self.cache_dir = cache_dir
        self.metadata_path = os.path.join(cache_dir, "candidate_features.parquet")

        start = time.time()
        self.selector = CandidateSelector(cache_dir=self.cache_dir)
        self.recruiter_engine = RecruiterIntelligenceEngine(
            metadata_parquet_path=self.metadata_path
        )
        self.behavior_engine = BehaviorIntelligenceEngine(
            metadata_parquet_path=self.metadata_path
        )
        self.explainability_engine = ExplainabilityEngine()
        self.startup_time = (time.time() - start) * 1000  # ms
        self.is_ready = True

    def run_pipeline(
        self, job_id: str, job_description: str
    ) -> List[SubmissionCandidate]:
        # 1. Retrieval
        retrieved = self.selector.retrieve(job_id, job_description)
        hybrid_scores = {c.candidate_id: c.hybrid_score for c in retrieved}

        faiss_scores = {c.candidate_id: c.faiss_score for c in retrieved}
        bm25_scores = {c.candidate_id: c.bm25_score for c in retrieved}

        # 2. Recruiter Intelligence
        recruiter_candidates = self.recruiter_engine.evaluate(retrieved)

        # 3. Behavior Intelligence
        behavior_candidates = self.behavior_engine.evaluate(recruiter_candidates)

        # 4. Final Ensemble
        ensemble_engine = FinalEnsembleEngine(hybrid_scores, faiss_scores, bm25_scores)
        ranked_candidates = ensemble_engine.evaluate(behavior_candidates)

        # 5. Explainability
        explained_candidates = self.explainability_engine.evaluate(ranked_candidates)

        # 6. Submission Mapping
        submission = self.explainability_engine.format_for_submission(
            explained_candidates
        )

        return submission

    def run_workspace(self, job_id: str, job_description: str) -> dict:
        start_time = time.time()

        # 1. Retrieval
        retrieved = self.selector.retrieve(job_id, job_description)
        hybrid_scores = {c.candidate_id: c.hybrid_score for c in retrieved}

        faiss_scores = {c.candidate_id: c.faiss_score for c in retrieved}
        bm25_scores = {c.candidate_id: c.bm25_score for c in retrieved}

        # 2. Recruiter Intelligence
        recruiter_candidates = self.recruiter_engine.evaluate(retrieved)

        # 3. Behavior Intelligence
        behavior_candidates = self.behavior_engine.evaluate(recruiter_candidates)

        # 4. Final Ensemble
        ensemble_engine = FinalEnsembleEngine(hybrid_scores, faiss_scores, bm25_scores)
        ranked_candidates = ensemble_engine.evaluate(behavior_candidates)

        # 5. Explainability
        explained_candidates = self.explainability_engine.evaluate(ranked_candidates)

        # 6. Submission Mapping
        submission = self.explainability_engine.format_for_submission(
            explained_candidates
        )

        # Aggregate Workspace Data
        pipeline_time = time.time() - start_time

        workspace_candidates = []
        for ec in explained_candidates:
            rc = ec.ranked_candidate
            workspace_candidates.append(
                {
                    "candidate_id": ec.candidate_id,
                    "overall_rank": ec.rank,
                    "final_score": ec.score,
                    "hybrid_score": rc.hybrid_score,
                    "faiss_score": rc.faiss_score,
                    "bm25_score": rc.bm25_score,
                    "recruiter_score": rc.recruiter_score,
                    "behavior_score": rc.behavior_score,
                    "ranking_breakdown": rc.ranking_breakdown,
                    "evidence_summary": [e.model_dump() for e in rc.evidence_summary],
                    "reasoning": ec.reasoning,
                    "positive_factors": ec.positive_factors,
                    "negative_factors": ec.negative_factors,
                }
            )

        total = len(workspace_candidates)
        avg_score = (
            sum(c["final_score"] for c in workspace_candidates) / total if total else 0
        )
        avg_hybrid = (
            sum(c["hybrid_score"] for c in workspace_candidates) / total if total else 0
        )
        avg_recruiter = (
            sum(c["recruiter_score"] for c in workspace_candidates) / total
            if total
            else 0
        )
        avg_behavior = (
            sum(c["behavior_score"] for c in workspace_candidates) / total
            if total
            else 0
        )

        # Generate Charts (Buckets)
        recruiter_dist = {"Poor": 0, "Fair": 0, "Strong": 0, "Exceptional": 0}
        for c in workspace_candidates:
            s = c["recruiter_score"]
            if s < settings.confidence_thresholds.medium:
                recruiter_dist["Poor"] += 1
            elif s < settings.confidence_thresholds.high:
                recruiter_dist["Fair"] += 1
            elif s < settings.confidence_thresholds.exceptional:
                recruiter_dist["Strong"] += 1
            else:
                recruiter_dist["Exceptional"] += 1

        behavior_dist = {"High Risk": 0, "Moderate Risk": 0, "Low Risk": 0, "Safe": 0}
        for c in workspace_candidates:
            s = c["behavior_score"]
            if s < settings.behavior.readiness_thresholds.passive:
                behavior_dist["High Risk"] += 1
            elif s < settings.behavior.readiness_thresholds.ready:
                behavior_dist["Moderate Risk"] += 1
            elif s < settings.behavior.readiness_thresholds.highly_ready:
                behavior_dist["Low Risk"] += 1
            else:
                behavior_dist["Safe"] += 1

        return {
            "job_summary": {
                "job_id": job_id,
                "job_description_length": len(job_description),
            },
            "pipeline_metrics": {
                "execution_time_ms": pipeline_time * 1000,
                "candidates_processed": total,
            },
            "dashboard_metrics": {
                "total_candidates": total,
                "avg_score": avg_score,
                "avg_hybrid": avg_hybrid,
                "avg_recruiter": avg_recruiter,
                "avg_behavior": avg_behavior,
            },
            "chart_data": {
                "recruiter_distribution": recruiter_dist,
                "behavior_distribution": behavior_dist,
            },
            "candidates": workspace_candidates,
            "submission_preview": [s.model_dump() for s in submission],
        }

    def explain(
        self, ranked_candidates: List[RankedCandidate]
    ) -> List[ExplainedCandidate]:
        """
        Runs the explainability engine on already-ranked candidates.
        """
        return self.explainability_engine.evaluate(ranked_candidates)
