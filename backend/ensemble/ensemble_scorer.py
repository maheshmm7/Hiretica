from typing import Dict, Tuple

from config.settings import EnsembleConfig


class EnsembleScorer:
    def __init__(self, config: EnsembleConfig):
        self.config = config

    def blend(
        self, hybrid_score: float, recruiter_score: float, behavior_score: float
    ) -> Tuple[float, Dict[str, float]]:

        score = (
            (hybrid_score * self.config.hybrid_retrieval)
            + (recruiter_score * self.config.recruiter_score)
            + (behavior_score * self.config.behavior_score)
        )

        # Normalize in case weights don't sum to 1.0
        total_weight = (
            self.config.hybrid_retrieval
            + self.config.recruiter_score
            + self.config.behavior_score
        )
        if total_weight > 0:
            score = score / total_weight

        score = min(max(score, 0.0), 1.0)

        breakdown = {
            "hybrid_contribution": hybrid_score * self.config.hybrid_retrieval,
            "recruiter_contribution": recruiter_score * self.config.recruiter_score,
            "behavior_contribution": behavior_score * self.config.behavior_score,
            "final_score": score,
        }

        return score, breakdown
