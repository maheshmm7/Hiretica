from typing import Any, Dict, List, Tuple


class ExperienceAnalyzer:
    def __init__(self, max_years: int = 20):
        self.max_years = max_years

    def analyze(
        self, features: Dict[str, Any]
    ) -> Tuple[float, float, float, List[Dict[str, Any]]]:
        evidence = []

        # 1. Total Years of Experience
        total_years = float(features.get("total_years_experience", 0.0))
        # Cap at max_years for scoring
        capped_years = min(total_years, self.max_years)
        experience_fit = capped_years / self.max_years if self.max_years > 0 else 0.0

        evidence.append(
            {
                "dimension": "experience_fit",
                "metric": "total_years",
                "value": experience_fit,
                "reason": f"Candidate has {total_years:.1f} years of experience (capped at {self.max_years} for scaling).",
            }
        )

        # 2. Production AI Score
        # Count of production AI keywords
        prod_ai = float(features.get("production_ai_score", 0.0))
        # Max out at 5 hits for a 1.0 score
        production_ai_score = min(prod_ai / 5.0, 1.0)

        if production_ai_score > 0:
            evidence.append(
                {
                    "dimension": "production_ai_score",
                    "metric": "production_keywords",
                    "value": production_ai_score,
                    "reason": f"Found {prod_ai} production engineering signals in past experiences.",
                }
            )

        # 3. Domain Relevance
        domain_relevance = 1.0 - float(features.get("research_ratio", 0.0))

        evidence.append(
            {
                "dimension": "domain_relevance",
                "metric": "industry_vs_research",
                "value": domain_relevance,
                "reason": f"Domain relevance is {domain_relevance:.2f} based on industry vs research ratio.",
            }
        )

        return experience_fit, production_ai_score, domain_relevance, evidence
