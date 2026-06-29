from typing import List, Tuple

from behavior.behavior_models import BehaviorEvidence


class EvidenceFormatter:
    """
    Standardizes and categorizes raw evidence into clean phrasing strings.
    """

    def extract_factors(
        self, evidence_list: List[BehaviorEvidence]
    ) -> Tuple[List[str], List[str]]:
        positive_factors = []
        negative_factors = []

        # Sort evidence by absolute impact descending so most impactful is first
        sorted_evidence = sorted(
            evidence_list, key=lambda e: abs(e.impact), reverse=True
        )

        for ev in sorted_evidence:
            if ev.impact > 0:
                positive_factors.append(self._format_positive(ev.reason))
            elif ev.impact < 0:
                negative_factors.append(self._format_negative(ev.reason))

        return positive_factors, negative_factors

    def _format_positive(self, raw_reason: str) -> str:
        # Lowercase and clean
        reason = raw_reason.lower().strip()

        # Map raw reasons to professional formatting
        if "high recruiter response" in reason:
            return "strong historical recruiter engagement"
        if "open to work" in reason:
            return "immediate availability"
        if "immediate notice" in reason:
            return "immediate notice period"
        if "highly validated" in reason:
            return "strong market validation"
        if "active profile" in reason:
            return "active open-source profile"

        return reason

    def _format_negative(self, raw_reason: str) -> str:
        reason = raw_reason.lower().strip()

        # Map raw reasons to professional, non-toxic formatting
        # Avoid bad, poor, weak, terrible, toxic, failed
        if "low recruiter response" in reason:
            return "limited historical recruiter engagement"
        if "not open" in reason:
            return "reduced availability likelihood"
        if "long notice" in reason:
            return "extended notice period"
        if "low market validation" in reason:
            return "lower market validation"
        if "incomplete profile" in reason:
            return "limited profile completeness"
        if "inactive profile" in reason:
            return "limited recent activity"

        return reason
