from typing import List

import pandas as pd

from config.settings import settings
from retrieval.retrieval_models import RetrievedCandidate

from .career_analysis import CareerAnalyzer
from .experience_analysis import ExperienceAnalyzer
from .leadership import LeadershipAnalyzer
from .recruiter_models import RecruiterCandidate
from .risk_engine import RiskEngine
from .score_blending import ScoreBlender
from .technical_fit import TechnicalFitAnalyzer


class RecruiterIntelligenceEngine:
    def __init__(self, metadata_parquet_path: str):
        # Load the feature dataset
        self.metadata = pd.read_parquet(metadata_parquet_path)
        self._id_to_idx = {
            cid: idx for idx, cid in enumerate(self.metadata["candidate_id"])
        }

        # Initialize sub-engines
        self.tech_analyzer = TechnicalFitAnalyzer()
        self.exp_analyzer = ExperienceAnalyzer(
            max_years=settings.thresholds.max_years_experience
        )
        self.career_analyzer = CareerAnalyzer(
            min_job_hopping_index=settings.thresholds.min_job_hopping_index
        )
        self.leadership_analyzer = LeadershipAnalyzer()
        self.risk_engine = RiskEngine(settings.risk_multipliers)
        self.blender = ScoreBlender(settings.intelligence.weights, settings.confidence_thresholds)

    def evaluate(
        self, retrieved_candidates: List[RetrievedCandidate]
    ) -> List[RecruiterCandidate]:
        recruiter_candidates = []

        for retrieved in retrieved_candidates:
            cid = retrieved.candidate_id

            # Fetch metadata features
            if cid in self._id_to_idx:
                idx = self._id_to_idx[cid]
                # Convert Pandas row to dict
                features = self.metadata.iloc[idx].to_dict()
            else:
                features = {}

            # 1. Technical Fit
            tech_fit, tech_ev = self.tech_analyzer.analyze(retrieved, features)

            # 2. Experience Fit
            exp_fit, prod_ai, dom_rel, exp_ev = self.exp_analyzer.analyze(features)

            # 3. Career Analysis
            car_prog, car_stab, growth, car_ev = self.career_analyzer.analyze(features)

            # 4. Leadership
            lead_score, lead_ev = self.leadership_analyzer.analyze(features)

            # 5. Risk Assessment
            risk_mult, risk_ev = self.risk_engine.analyze(features)

            # 6. Final Blending
            base_score, final_score, conf_band, breakdown = self.blender.blend(
                technical_fit=tech_fit,
                experience_fit=exp_fit,
                career_progression=car_prog,
                leadership_score=lead_score,
                domain_relevance=dom_rel,
                career_stability=car_stab,
                growth_trend=growth,
                risk_multiplier=risk_mult,
            )

            evidence_log = tech_ev + exp_ev + car_ev + lead_ev + risk_ev

            # 7. Construct final RecruiterCandidate
            rc = RecruiterCandidate(
                candidate_id=cid,
                faiss_score=retrieved.faiss_score,
                bm25_score=retrieved.bm25_score,
                hybrid_score=retrieved.hybrid_score,
                technical_fit=tech_fit,
                experience_fit=exp_fit,
                career_progression=car_prog,
                leadership_score=lead_score,
                production_ai_score=prod_ai,
                retrieval_experience=False,  # Could be derived from DB
                vector_database_experience=features.get("vector_db_experience", False)
                == "true",
                evaluation_framework_score=0.0,
                domain_relevance=dom_rel,
                career_stability=car_stab,
                growth_trend=growth,
                risk_multiplier=risk_mult,
                recruiter_confidence=base_score,  # Using base_score as the pre-risk confidence
                confidence_band=conf_band,
                base_recruiter_score=base_score,
                recruiter_score=final_score,
                score_breakdown=breakdown,
                evidence=evidence_log,
            )

            recruiter_candidates.append(rc)

        # Sort by final recruiter score descending
        recruiter_candidates.sort(key=lambda x: x.recruiter_score, reverse=True)
        return recruiter_candidates
