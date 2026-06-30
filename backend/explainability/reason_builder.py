from typing import Tuple

from .template_engine import TemplateEngine


class ReasonBuilder:
    def __init__(self):
        self.template_engine = TemplateEngine()
        self.MAX_LENGTH = 250

    def build_reason(
        self,
        tech_score: float,
        behavior_score: float,
        positive_factors: list,
        negative_factors: list,
    ) -> Tuple[str, str]:

        has_pos = len(positive_factors) > 0
        has_neg = len(negative_factors) > 0

        # 1. Select template
        template_id = self.template_engine.select_template(
            tech_score=tech_score,
            behavior_score=behavior_score,
            has_positive=has_pos,
            has_negative=has_neg,
        )

        # Seed based on scores for deterministic variance
        seed = tech_score + behavior_score

        # 2. Render initial string
        reasoning = self.template_engine.render(
            template_id=template_id,
            pos_factors=positive_factors,
            neg_factors=negative_factors,
            seed=seed,
        )

        # 3. Enforce maximum length constraint
        # If it exceeds 250 characters, we try removing factors rather than truncating
        if len(reasoning) > self.MAX_LENGTH:
            # Fallback to the simplest possible explanation
            template_id = "default_positive"
            reasoning = self.template_engine.render(
                template_id=template_id,
                pos_factors=positive_factors,
                neg_factors=[],
                seed=seed,
            )

            # If STILL too long, truncate with ellipsis
            # (should not happen with basic templates)
            if len(reasoning) > self.MAX_LENGTH:
                reasoning = reasoning[: self.MAX_LENGTH - 3] + "..."

        return reasoning, template_id
