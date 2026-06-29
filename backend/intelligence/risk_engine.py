from typing import Any, Dict, List, Tuple

from config.settings import RiskMultipliersConfig


class RiskEngine:
    def __init__(self, config: RiskMultipliersConfig):
        self.config = config

    def analyze(self, features: Dict[str, Any]) -> Tuple[float, List[Dict[str, Any]]]:
        evidence = []

        # Default Low Risk
        risk_multiplier = self.config.low

        # 1. Inactivity Risk
        days_inactive = float(features.get("days_since_active", 0.0))
        if days_inactive > 365:
            risk_multiplier = min(risk_multiplier, self.config.critical)
            evidence.append(
                {
                    "dimension": "risk",
                    "metric": "inactivity",
                    "value": risk_multiplier,
                    "reason": f"Critical Risk: Candidate inactive for {days_inactive} days.",
                }
            )
        elif days_inactive > 180:
            risk_multiplier = min(risk_multiplier, self.config.high)
            evidence.append(
                {
                    "dimension": "risk",
                    "metric": "inactivity",
                    "value": risk_multiplier,
                    "reason": f"High Risk: Candidate inactive for {days_inactive} days.",
                }
            )

        # 2. Honeypot/Impossible Data Risk
        honeypot_score = float(features.get("honeypot_risk_score", 0.0))
        if honeypot_score > 0.8:
            risk_multiplier = min(risk_multiplier, self.config.critical)
            evidence.append(
                {
                    "dimension": "risk",
                    "metric": "honeypot",
                    "value": risk_multiplier,
                    "reason": f"Critical Risk: Highly probable fabricated data (Score {honeypot_score:.2f}).",
                }
            )

        # 3. Flake Risk
        recruiter_response_rate = float(features.get("recruiter_response_rate", 1.0))
        if recruiter_response_rate < 0.2:
            risk_multiplier = min(risk_multiplier, self.config.medium)
            evidence.append(
                {
                    "dimension": "risk",
                    "metric": "flake_risk",
                    "value": risk_multiplier,
                    "reason": f"Medium Risk: Historically poor recruiter response rate ({recruiter_response_rate:.1%}).",
                }
            )

        if not evidence:
            evidence.append(
                {
                    "dimension": "risk",
                    "metric": "baseline",
                    "value": risk_multiplier,
                    "reason": "Low Risk: No significant risk flags detected.",
                }
            )

        return risk_multiplier, evidence
