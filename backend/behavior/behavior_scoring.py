from typing import Dict, Tuple

from config.settings import BehaviorWeightsConfig


class BehaviorScorer:
    def __init__(self, weights: BehaviorWeightsConfig):
        self.weights = weights

    def blend(
        self,
        engagement_score: float,
        availability_score: float,
        profile_quality_score: float,
    ) -> Tuple[float, Dict[str, float]]:

        score = (
            (engagement_score * self.weights.engagement)
            + (availability_score * self.weights.availability)
            + (profile_quality_score * self.weights.profile_quality)
        )

        # Normalize in case weights don't sum to 1.0
        total_weight = (
            self.weights.engagement
            + self.weights.availability
            + self.weights.profile_quality
        )
        if total_weight > 0:
            score = score / total_weight

        score = min(max(score, 0.0), 1.0)

        breakdown = {
            "engagement_score": engagement_score,
            "availability_score": availability_score,
            "profile_quality_score": profile_quality_score,
            "behavior_score": score,
        }

        return score, breakdown
