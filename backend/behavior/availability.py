from typing import Any, Dict, List, Tuple

from .behavior_models import BehaviorEvidence


class AvailabilityAnalyzer:
    def analyze(
        self, features: Dict[str, Any]
    ) -> Tuple[float, List[BehaviorEvidence], List[str]]:
        evidence = []
        flags = []

        # Open to work flag
        open_to_work = features.get("open_to_work", False)
        if isinstance(open_to_work, str):
            open_to_work = open_to_work.lower() == "true"

        score = 0.5
        if open_to_work:
            score = 1.0
            evidence.append(
                BehaviorEvidence(
                    module="availability",
                    reason="Candidate is explicitly marked as open to work.",
                    impact=0.5,
                )
            )
        else:
            evidence.append(
                BehaviorEvidence(
                    module="availability",
                    reason="Candidate is not currently marked as open to work.",
                    impact=-0.5,
                )
            )

        # Notice period mapping
        notice_period = features.get("notice_period_category", "unknown")
        notice_map = {
            "<30": 1.0,
            "30-60": 0.8,
            "60-90": 0.5,
            ">90": 0.2,
            "unknown": 0.5,
        }

        notice_score = notice_map.get(notice_period, 0.5)
        evidence.append(
            BehaviorEvidence(
                module="availability",
                reason=f"Notice period category is {notice_period}.",
                impact=notice_score - 0.5,
            )
        )

        if notice_period == ">90":
            flags.append("Long Notice Period")

        final_score = (score + notice_score) / 2.0
        return final_score, evidence, flags
