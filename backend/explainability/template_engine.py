import random
import re


class TemplateEngine:
    """
    Deterministically selects templates based on the profile of the candidate.
    """

    TEMPLATES = {
        "strong_all": [
            "{pos1}. Displays strong potential for this position.",
            "{pos1}. Recommended for recruiter outreach.",
            "{pos1}. Represents a solid fit for the role.",
            "{pos1}. Highly competitive profile."
        ],
        "moderate_overall": [
            "{pos1}. Good overall fit based on the available profile.",
            "{pos1}. Consistent professional background.",
            "{pos1}. Indicates a solid baseline fit for the position.",
            "{pos1}."
        ],
        "strong_tech_behavioral_risk": [
            "{pos1}. Note: {neg1}.",
            "{pos1}. Verify during outreach: {neg1}.",
            "{pos1}. {neg1}.",
            "{pos1}. Consideration needed: {neg1}."
        ],
        "high_behavior_limited_tech": [
            "{pos1}. Demonstrates strong foundational potential.",
            "{pos1}. Good overall fit despite some technical gaps.",
            "{pos1}. Solid professional background.",
            "{pos1}."
        ],
        "default_positive": [
            "{pos1}.",
            "{pos1}. Good overall fit.",
            "{pos1}. Consistent professional background.",
            "{pos1}. Recommended for further review."
        ],
        "default_mixed": [
            "{pos1}. {neg1}.",
            "{pos1}. Please note: {neg1}.",
            "{pos1}. Consideration needed: {neg1}.",
            "{pos1}. Verify during outreach: {neg1}."
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
            # remove redundant risk/multiplier words
            f_str = re.sub(
                r"(?i)\b(critical risk|high risk|medium risk|low risk|risk multiplier|risk score|multiplier)\b[:\s]*[\d\.]*",
                "",
                f_str,
            )
            # Remove leading hyphens or spaces
            f_str = re.sub(r"^\W+", "", f_str)
            # clean up whitespace and punctuation
            f_str = re.sub(r"\s+", " ", f_str)
            f_str = f_str.rstrip(".,;: \t\n\r")
            # Capitalize first letter
            if f_str:
                f_str = f_str[0].upper() + f_str[1:]
            return f_str

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
