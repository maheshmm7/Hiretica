import time
from typing import List

from ensemble.ensemble_models import RankedCandidate, SubmissionCandidate

from .evidence_formatter import EvidenceFormatter
from .explanation_models import ExplainedCandidate, ExplanationMetadata
from .reason_builder import ReasonBuilder


class ExplainabilityEngine:
    def __init__(self):
        self.formatter = EvidenceFormatter()
        self.builder = ReasonBuilder()

    def evaluate(
        self, ranked_candidates: List[RankedCandidate]
    ) -> List[ExplainedCandidate]:
        explained_list = []

        for rc in ranked_candidates:
            start_time = time.time()

            # 1. Format evidence
            positive_factors, negative_factors = self.formatter.extract_factors(
                rc.evidence_summary
            )

            # 2. Build reasoning string
            reasoning, template_id = self.builder.build_reason(
                tech_score=rc.recruiter_score,
                behavior_score=rc.behavior_score,
                positive_factors=positive_factors,
                negative_factors=negative_factors,
            )

            generation_time = (time.time() - start_time) * 1000  # ms

            # 3. Build Metadata
            metadata = ExplanationMetadata(
                template_id=template_id,
                evidence_used=min(1, len(positive_factors))
                + min(1, len(negative_factors)),
                generated_length=len(reasoning),
                generation_time_ms=generation_time,
            )

            # 4. Construct ExplainedCandidate
            ec = ExplainedCandidate(
                candidate_id=rc.candidate_id,
                rank=rc.overall_rank,
                score=rc.final_hiretica_score,
                reasoning=reasoning,
                positive_factors=positive_factors,
                negative_factors=negative_factors,
                explanation_metadata=metadata,
                ranked_candidate=rc,
            )

            explained_list.append(ec)

        return explained_list

    def format_for_submission(
        self, explained_candidates: List[ExplainedCandidate], top_k: int = 100
    ) -> List[SubmissionCandidate]:
        submission = []
        for ec in explained_candidates[:top_k]:
            sc = SubmissionCandidate(
                candidate_id=ec.candidate_id,
                rank=ec.rank,
                score=ec.score,
                reasoning=ec.reasoning,
            )
            submission.append(sc)
        return submission
