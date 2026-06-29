


class TemplateEngine:
    """
    Deterministically selects templates based on the profile of the candidate.
    """

    TEMPLATES = {
        "strong_all": "Demonstrates strong technical alignment alongside {pos1}.",
        "strong_all_2": (
            "Highly competitive candidate featuring strong technical fit and {pos1}."
        ),
        "moderate_overall": "Shows moderate technical alignment, supported by {pos1}.",
        "strong_tech_behavioral_risk": (
            "Presents strong technical capability, though marked by {neg1} considerations."
        ),
        "strong_tech_behavioral_risk_2": (
            "Solid technical alignment, with additional consideration needed for {neg1}."
        ),
        "high_behavior_limited_tech": (
            "Exhibits {pos1}, with slightly lower technical alignment."
        ),
        "default_positive": "Profile is characterized by {pos1}.",
        "default_mixed": "Displays {pos1}, balanced by {neg1} considerations.",
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
            # Deterministically cycle or just pick one
            # We can use the tech_score decimal to pick if we want variance
            return "strong_all" if int(tech_score * 100) % 2 == 0 else "strong_all_2"

        if is_strong_tech and has_negative:
            return (
                "strong_tech_behavioral_risk"
                if int(tech_score * 100) % 2 == 0
                else "strong_tech_behavioral_risk_2"
            )

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

    def render(self, template_id: str, pos_factors: list, neg_factors: list) -> str:
        template_str = self.TEMPLATES.get(
            template_id, self.TEMPLATES["default_positive"]
        )

        # Safely get variables
        pos1 = pos_factors[0] if pos_factors else "solid overall background"
        neg1 = neg_factors[0] if neg_factors else "minor"

        rendered = template_str.format(pos1=pos1, neg1=neg1)

        # Ensure it always starts with capital
        if rendered:
            rendered = rendered[0].upper() + rendered[1:]

        return rendered
