from typing import Any, Dict, List, Tuple

from .behavior_models import BehaviorEvidence


class ProfileQualityAnalyzer:
    def analyze(
        self, features: Dict[str, Any]
    ) -> Tuple[float, List[BehaviorEvidence], List[str]]:
        evidence = []
        flags = []

        # 1. Market Validation (saved by recruiters)
        saved = float(features.get("saved_by_recruiters_30d", 0))
        market_score = min(saved / 10.0, 1.0)

        if market_score > 0.5:
            evidence.append(
                BehaviorEvidence(
                    module="profile_quality",
                    reason=(
                        f"High market validation: Saved by {saved} "
                        "recruiters recently."
                    ),
                    impact=0.5,
                )
            )
        elif market_score == 0:
            flags.append("Low Market Validation")
            evidence.append(
                BehaviorEvidence(
                    module="profile_quality",
                    reason="No recent recruiter saves detected.",
                    impact=0.0,
                )
            )

        # 2. Profile completeness (proxy via available fields)
        # Check if they have github activity or other fields
        has_github = features.get("github_commits_90d", 0) > 0
        github_score = 1.0 if has_github else 0.5

        if has_github:
            evidence.append(
                BehaviorEvidence(
                    module="profile_quality",
                    reason="Candidate has active GitHub contributions.",
                    impact=0.5,
                )
            )
        else:
            flags.append("Incomplete Profile")

        score = (market_score * 0.5) + (github_score * 0.5)
        return score, evidence, flags
