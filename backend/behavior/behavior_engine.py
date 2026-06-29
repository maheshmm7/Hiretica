from typing import List

import pandas as pd

from config.settings import settings
from intelligence.recruiter_models import RecruiterCandidate

from .availability import AvailabilityAnalyzer
from .behavior_models import BehaviorCandidate
from .behavior_scoring import BehaviorScorer
from .engagement import EngagementAnalyzer
from .hiring_readiness import HiringReadinessMapper
from .profile_quality import ProfileQualityAnalyzer


class BehaviorIntelligenceEngine:
    def __init__(self, metadata_parquet_path: str):
        self.metadata = pd.read_parquet(metadata_parquet_path)
        self._id_to_idx = {
            cid: idx for idx, cid in enumerate(self.metadata["candidate_id"])
        }

        self.engagement = EngagementAnalyzer()
        self.availability = AvailabilityAnalyzer()
        self.profile = ProfileQualityAnalyzer()
        self.scorer = BehaviorScorer(settings.behavior.weights)
        self.readiness_mapper = HiringReadinessMapper(
            settings.behavior.readiness_thresholds, settings.behavior.critical_risk_cap
        )

    def evaluate(
        self, recruiter_candidates: List[RecruiterCandidate]
    ) -> List[BehaviorCandidate]:
        behavior_candidates = []

        for rec in recruiter_candidates:
            cid = rec.candidate_id

            if cid in self._id_to_idx:
                idx = self._id_to_idx[cid]
                features = self.metadata.iloc[idx].to_dict()
            else:
                features = {}

            # Analyze
            eng_score, eng_ev, eng_flags = self.engagement.analyze(features)
            avail_score, avail_ev, avail_flags = self.availability.analyze(features)
            prof_score, prof_ev, prof_flags = self.profile.analyze(features)

            # Blend
            behavior_score, breakdown = self.scorer.blend(
                eng_score, avail_score, prof_score
            )

            # Determine readiness cap condition (Phase B7A risk multiplier check)
            # If critical risk config is 0.60, and rec risk multiplier <= 0.60, cap them
            is_critical = rec.risk_multiplier <= settings.risk_multipliers.critical

            readiness = self.readiness_mapper.map_readiness(behavior_score, is_critical)

            all_evidence = eng_ev + avail_ev + prof_ev
            all_flags = eng_flags + avail_flags + prof_flags

            # Use behavior score as confidence
            behavior_confidence = behavior_score

            bc = BehaviorCandidate(
                candidate_id=cid,
                recruiter_score=rec.recruiter_score,
                recruiter_risk_multiplier=rec.risk_multiplier,
                availability_score=avail_score,
                engagement_score=eng_score,
                profile_quality_score=prof_score,
                behavior_score=behavior_score,
                behavior_confidence=behavior_confidence,
                hiring_readiness=readiness,
                behavior_breakdown=breakdown,
                behavior_evidence=all_evidence,
                behavior_flags=all_flags,
            )

            behavior_candidates.append(bc)

        return behavior_candidates
