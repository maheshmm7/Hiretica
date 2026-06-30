from typing import Dict, Tuple

from config.settings import ConfidenceThresholdsConfig, IntelligenceWeights


class ScoreBlender:
    def __init__(
        self, weights: IntelligenceWeights, thresholds: ConfidenceThresholdsConfig
    ):
        self.weights = weights
        self.thresholds = thresholds

    def get_confidence_band(self, base_score: float) -> str:
        if base_score >= self.thresholds.exceptional:
            return "Exceptional"
        elif base_score >= self.thresholds.high:
            return "High"
        elif base_score >= self.thresholds.medium:
            return "Medium"
        else:
            return "Low"

    def blend(
        self,
        technical_fit: float,
        experience_fit: float,
        career_progression: float,
        leadership_score: float,
        domain_relevance: float,
        career_stability: float,
        growth_trend: float,
        risk_multiplier: float,
    ) -> Tuple[float, float, str, Dict[str, float]]:

        # 1. Compute Base Recruiter Score (Weighted Arithmetic Mean)
        base_score = (
            (technical_fit * self.weights.technical_fit)
            + (experience_fit * self.weights.experience_fit)
            + (career_progression * self.weights.career_progression)
            + (leadership_score * self.weights.leadership)
            + (domain_relevance * self.weights.domain_relevance)
            + (career_stability * self.weights.career_stability)
            + (growth_trend * self.weights.growth_trend)
        )

        # Normalize in case weights don't perfectly sum to 1.0 (though they should)
        total_weight = (
            self.weights.technical_fit
            + self.weights.experience_fit
            + self.weights.career_progression
            + self.weights.leadership
            + self.weights.domain_relevance
            + self.weights.career_stability
            + self.weights.growth_trend
        )
        if total_weight > 0:
            base_score = base_score / total_weight

        base_score = min(max(base_score, 0.0), 1.0)

        # 2. Assign Confidence Band based on Base Score
        confidence_band = self.get_confidence_band(base_score)

        # 3. Apply Multiplicative Risk Penalty
        recruiter_score = base_score * risk_multiplier

        score_breakdown = {
            "technical_fit": technical_fit,
            "experience_fit": experience_fit,
            "career_progression": career_progression,
            "leadership": leadership_score,
            "domain_relevance": domain_relevance,
            "career_stability": career_stability,
            "growth_trend": growth_trend,
            "base_recruiter_score": base_score,
            "risk_multiplier": risk_multiplier,
            "recruiter_score": recruiter_score,
        }

        return base_score, recruiter_score, confidence_band, score_breakdown
