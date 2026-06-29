import os
import time
from typing import List

from behavior.behavior_engine import BehaviorIntelligenceEngine
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

        # 2. Recruiter Intelligence
        recruiter_candidates = self.recruiter_engine.evaluate(retrieved)

        # 3. Behavior Intelligence
        behavior_candidates = self.behavior_engine.evaluate(recruiter_candidates)

        # 4. Final Ensemble
        ensemble_engine = FinalEnsembleEngine(hybrid_scores)
        ranked_candidates = ensemble_engine.evaluate(behavior_candidates)

        # 5. Explainability
        explained_candidates = self.explainability_engine.evaluate(ranked_candidates)

        # 6. Submission Mapping
        submission = self.explainability_engine.format_for_submission(
            explained_candidates
        )

        return submission

    def explain(
        self, ranked_candidates: List[RankedCandidate]
    ) -> List[ExplainedCandidate]:
        """
        Runs the explainability engine on already-ranked candidates.
        """
        return self.explainability_engine.evaluate(ranked_candidates)
