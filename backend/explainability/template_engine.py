import random
import re


class TemplateEngine:
    """
    Deterministically selects templates based on the profile of the candidate.
    """

    TEMPLATES = {
        "strong_all": [
            "Demonstrates exceptional technical alignment alongside {pos1}.",
            "A highly competitive candidate featuring a strong technical fit and {pos1}.",
            "Presents a robust technical profile complemented by {pos1}.",
        ],
        "moderate_overall": [
            "Shows moderate technical alignment, supported by {pos1}.",
            "Exhibits a balanced technical foundation alongside {pos1}.",
            "A solid technical baseline, further enhanced by {pos1}.",
        ],
        "strong_tech_behavioral_risk": [
            "Presents strong technical capability, though marked by {neg1} considerations.",
            "Solid technical alignment, with additional consideration needed for {neg1}.",
            "Technically proficient, however, {neg1} may require attention.",
        ],
        "high_behavior_limited_tech": [
            "Exhibits {pos1}, with slightly lower technical alignment.",
            "Demonstrates {pos1} which partially offsets moderate technical fit.",
            "Strong behavioral indicators including {pos1}, despite lower technical match.",
        ],
        "default_positive": [
            "Profile is characterized by {pos1}.",
            "Candidate demonstrates {pos1}.",
            "Notable strengths include {pos1}.",
        ],
        "default_mixed": [
            "Displays {pos1}, balanced by {neg1} considerations.",
            "Shows {pos1}, while presenting {neg1} factors.",
            "A mixed profile showing {pos1}, but with {neg1}.",
        ],
    }

    def select_template(
        self,
        tech_score: float,
        behavior_score: float,
        has_positive: bool,
        has_negative: bool,
    ) -> str:
        # High threshold for "strong"
        is_strong_tech = tech_score >= 0.7
        is_strong_behavior = behavior_score >= 0.7

        is_moderate_tech = 0.4 <= tech_score < 0.7

        if is_strong_tech and is_strong_behavior and has_positive:
            return "strong_all"

        if is_strong_tech and has_negative:
            return "strong_tech_behavioral_risk"

        if is_moderate_tech and has_positive:
            return "moderate_overall"

        if not is_strong_tech and is_strong_behavior and has_positive:
            return "high_behavior_limited_tech"

        if has_positive and has_negative:
            return "default_mixed"

        if has_positive:
            return "default_positive"

        # Fallback if no specific template hits
        return "default_positive"

    def render(
        self, template_id: str, pos_factors: list, neg_factors: list, seed: float = 0.0
    ) -> str:
        templates = self.TEMPLATES.get(template_id, self.TEMPLATES["default_positive"])

        # Deterministically select a variation based on the seed
        variation_idx = int(seed * 100) % len(templates)
        template_str = templates[variation_idx]

        # Safely get variables, strictly stripping trailing punctuation to avoid duplicate dots.
        # Synthesize raw signals into cohesive phrasing

        def clean_factor(f, default_val):
            if not f:
                return default_val
            # convert lists or dicts to string if they are raw signals
            f_str = str(f).strip()
            # remove redundant risk/multiplier words if they don't fit grammatically
            f_str = re.sub(
                r"(?i)\b(risk multiplier|risk score|multiplier)\b[:\s]*[\d\.]+",
                "",
                f_str,
            )
            # clean up whitespace and punctuation
            f_str = re.sub(r"\s+", " ", f_str)
            return f_str.rstrip(".,;: \t\n\r")

        pos1 = clean_factor(
            pos_factors[0] if pos_factors else None, "a solid overall background"
        )
        neg1 = clean_factor(
            neg_factors[0] if neg_factors else None, "minor risk factors"
        )

        rendered = template_str.format(pos1=pos1, neg1=neg1)

        # Fix punctuation issues (multiple dots, spaces before dot)
        rendered = re.sub(r"\s+\.", ".", rendered)
        rendered = re.sub(r"\.{2,}", ".", rendered)

        # Ensure it always starts with capital and ends with exactly one period
        if rendered:
            rendered = rendered[0].upper() + rendered[1:]
            if not rendered.endswith("."):
                rendered += "."

        return rendered
