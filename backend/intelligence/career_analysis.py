from typing import Any, Dict, List, Tuple


class CareerAnalyzer:
    def __init__(self, min_job_hopping_index: float = 1.5):
        self.min_job_hopping_index = min_job_hopping_index

    def analyze(
        self, features: Dict[str, Any]
    ) -> Tuple[float, float, float, List[Dict[str, Any]]]:
        evidence = []

        # 1. Career Stability
        jhi = float(features.get("job_hopping_index", 0.0))

        if jhi == 0:
            career_stability = 0.5  # Default middle ground for no data
        elif jhi < self.min_job_hopping_index:
            # Penalize stability if they job hop too much
            career_stability = max(jhi / self.min_job_hopping_index, 0.0)
            evidence.append(
                {
                    "dimension": "career_stability",
                    "metric": "job_hopping_index",
                    "value": career_stability,
                    "reason": f"High job hopping risk detected (Index: {jhi:.2f}).",
                }
            )
        else:
            # Good stability
            # Scale up to 1.0 slowly
            career_stability = min(jhi / (self.min_job_hopping_index * 3), 1.0)
            career_stability = max(
                career_stability, 0.7
            )  # Base for being above threshold
            evidence.append(
                {
                    "dimension": "career_stability",
                    "metric": "job_hopping_index",
                    "value": career_stability,
                    "reason": f"Stable career trajectory (Index: {jhi:.2f}).",
                }
            )

        # 2. Career Progression (Simplified mock for now based on title relevance)
        # In a real model, this would track Junior -> Mid -> Senior transitions
        current_title_rel = float(features.get("current_title_relevance", 0.0))
        career_progression = min(max(current_title_rel, 0.0), 1.0)

        evidence.append(
            {
                "dimension": "career_progression",
                "metric": "current_title_momentum",
                "value": career_progression,
                "reason": f"Current title aligns closely with target trajectory ({career_progression:.2f}).",
            }
        )

        # 3. Growth Trend
        # Proxy growth trend through career progression and stability interplay
        growth_trend = (career_progression * 0.7) + (career_stability * 0.3)

        return career_progression, career_stability, growth_trend, evidence
