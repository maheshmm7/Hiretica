import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config.settings import (ConfidenceThresholdsConfig, IntelligenceWeights,
                             RiskMultipliersConfig)
from intelligence.risk_engine import RiskEngine
from intelligence.score_blending import ScoreBlender


def test_score_blender():
    weights = IntelligenceWeights(
        technical_fit=0.35,
        experience_fit=0.20,
        career_progression=0.15,
        leadership=0.10,
        domain_relevance=0.10,
        career_stability=0.05,
        growth_trend=0.05,
    )
    thresholds = ConfidenceThresholdsConfig(exceptional=0.85, high=0.7, medium=0.5)
    blender = ScoreBlender(weights, thresholds)

    base_score, rec_score, conf_band, breakdown = blender.blend(
        technical_fit=1.0,
        experience_fit=1.0,
        career_progression=1.0,
        leadership_score=1.0,
        domain_relevance=1.0,
        career_stability=1.0,
        growth_trend=1.0,
        risk_multiplier=0.8,  # High Risk
    )

    assert base_score == pytest.approx(1.0)
    assert rec_score == pytest.approx(0.8)
    assert conf_band == "Exceptional"  # Base score is 1.0 > 0.85
    assert breakdown["recruiter_score"] == pytest.approx(0.8)


def test_risk_engine():
    config = RiskMultipliersConfig(low=1.0, medium=0.92, high=0.8, critical=0.6)
    engine = RiskEngine(config)

    # 1. Low risk
    mult, ev = engine.analyze({"days_since_active": 10})
    assert mult == 1.0

    # 2. Inactivity risk
    mult, ev = engine.analyze({"days_since_active": 200})
    assert mult == 0.8

    # 3. Flake risk
    mult, ev = engine.analyze({"recruiter_response_rate": 0.1})
    assert mult == 0.92

    # 4. Critical Honeypot risk overrides
    mult, ev = engine.analyze({"honeypot_risk_score": 0.9, "days_since_active": 10})
    assert mult == 0.6
