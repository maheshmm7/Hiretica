from typing import Any, Dict, List, Tuple

from .behavior_models import BehaviorEvidence


class EngagementAnalyzer:
    def analyze(
        self, features: Dict[str, Any]
    ) -> Tuple[float, List[BehaviorEvidence], List[str]]:
        evidence = []
        flags = []

        # 1. Recruiter Response Rate
        response_rate = float(
            features.get("recruiter_response_rate", 0.5)
        )  # Default to middle ground if unknown
        score = response_rate

        evidence.append(
            BehaviorEvidence(
                module="engagement",
                reason=f"Historical recruiter response rate is {response_rate:.0%}.",
                impact=score,
            )
        )

        if response_rate < 0.2:
            flags.append("Low Recruiter Response")

        # 2. Days Since Active
        days_inactive = float(features.get("days_since_active", 90.0))
        if days_inactive > 180:
            score = score * 0.5
            evidence.append(
                BehaviorEvidence(
                    module="engagement",
                    reason=f"Candidate has been inactive for {days_inactive} days.",
                    impact=-0.5,
                )
            )
            flags.append("Inactive Profile")
        elif days_inactive < 30:
            score = min(score + 0.2, 1.0)
            evidence.append(
                BehaviorEvidence(
                    module="engagement",
                    reason="Candidate was active in the last 30 days.",
                    impact=0.2,
                )
            )

        return score, evidence, flags
