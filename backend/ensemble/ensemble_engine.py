from typing import List

from behavior.behavior_models import BehaviorCandidate
from config.settings import settings

from .ensemble_models import RankedCandidate, SubmissionCandidate
from .ensemble_scorer import EnsembleScorer


class FinalEnsembleEngine:
    def __init__(self, hybrid_scores: dict):
        self.scorer = EnsembleScorer(settings.ensemble)
        # hybrid_scores is a dict mapping candidate_id to hybrid_score
        # because the BehaviorCandidate doesn't carry hybrid_score natively
        # unless we explicitly pull it from the metadata.
        self.hybrid_scores = hybrid_scores

    def evaluate(
        self, behavior_candidates: List[BehaviorCandidate]
    ) -> List[RankedCandidate]:
        ranked_candidates = []

        for bc in behavior_candidates:
            hybrid_score = self.hybrid_scores.get(bc.candidate_id, 0.0)

            final_score, breakdown = self.scorer.blend(
                hybrid_score=hybrid_score,
                recruiter_score=bc.recruiter_score,
                behavior_score=bc.behavior_score,
            )

            # Aggregate evidence
            # In a real system, we'd also pull recruiter evidence,
            # but we have behavior_evidence
            # We can just use the behavior evidence for now.
            evidence_summary = bc.behavior_evidence

            rc = RankedCandidate(
                candidate_id=bc.candidate_id,
                hybrid_score=hybrid_score,
                recruiter_score=bc.recruiter_score,
                behavior_score=bc.behavior_score,
                final_hiretica_score=final_score,
                ranking_breakdown=breakdown,
                evidence_summary=evidence_summary,
                overall_rank=0,  # will be updated after sorting
            )

            ranked_candidates.append(rc)

        # Sort monotonically descending
        ranked_candidates.sort(key=lambda x: x.final_hiretica_score, reverse=True)

        # Assign ranks
        final_ranked = []
        for rank, rc in enumerate(ranked_candidates, start=1):
            rc_dict = rc.model_dump()
            rc_dict["overall_rank"] = rank
            final_ranked.append(RankedCandidate(**rc_dict))

        return final_ranked

    def format_for_submission(
        self, ranked_candidates: List[RankedCandidate], top_k: int = 100
    ) -> List[SubmissionCandidate]:
        submission = []
        for rc in ranked_candidates[:top_k]:
            sc = SubmissionCandidate(
                candidate_id=rc.candidate_id,
                rank=rc.overall_rank,
                score=rc.final_hiretica_score,
                reasoning=None,  # Placeholder for Explainability Phase B9
            )
            submission.append(sc)
        return submission
