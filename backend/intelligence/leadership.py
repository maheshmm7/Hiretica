from typing import Any, Dict, List, Tuple


class LeadershipAnalyzer:
    def __init__(self):
        pass

    def analyze(self, features: Dict[str, Any]) -> Tuple[float, List[Dict[str, Any]]]:
        evidence = []

        # In absence of direct leadership metadata, we can extract it from
        # features if they exist (e.g., 'leadership_keywords_count').
        # For now, we will use a base of 0.5 and add boosts if they have experience.
        total_exp = float(features.get("total_years_experience", 0.0))

        # Rough heuristic: More experience implicitly yields higher baseline leadership potential
        leadership_score = min(total_exp / 15.0, 1.0) * 0.7

        # If there are explicit leadership features (e.g., managed_team_size)
        if features.get("managed_team_size", 0) > 0:
            leadership_score = min(leadership_score + 0.3, 1.0)
            evidence.append(
                {
                    "dimension": "leadership",
                    "metric": "managed_teams",
                    "value": leadership_score,
                    "reason": "Candidate has explicit management experience.",
                }
            )
        else:
            evidence.append(
                {
                    "dimension": "leadership",
                    "metric": "inferred_leadership",
                    "value": leadership_score,
                    "reason": f"Leadership potential inferred from {total_exp:.1f} years of experience.",
                }
            )

        return leadership_score, evidence
