import pytest

from behavior.behavior_scoring import BehaviorScorer
from behavior.hiring_readiness import HiringReadinessMapper
from config.settings import BehaviorWeightsConfig, ReadinessThresholdsConfig


def test_hiring_readiness_mapper():
    thresholds = ReadinessThresholdsConfig(highly_ready=0.7, ready=0.5, passive=0.3)
    mapper = HiringReadinessMapper(thresholds, critical_risk_cap="Ready")

    # Not critical risk
    assert mapper.map_readiness(0.8, False) == "Highly Ready"
    assert mapper.map_readiness(0.6, False) == "Ready"
    assert mapper.map_readiness(0.4, False) == "Passive"
    assert mapper.map_readiness(0.2, False) == "Unlikely"

    # Critical risk caps it at "Ready"
    assert mapper.map_readiness(0.8, True) == "Ready"  # Capped
    assert mapper.map_readiness(0.6, True) == "Ready"
    assert mapper.map_readiness(0.4, True) == "Passive"
    assert mapper.map_readiness(0.2, True) == "Unlikely"


def test_behavior_scoring():
    weights = BehaviorWeightsConfig(
        engagement=0.4, availability=0.4, profile_quality=0.2
    )
    scorer = BehaviorScorer(weights)

    # Max score
    score, breakdown = scorer.blend(1.0, 1.0, 1.0)
    assert abs(score - 1.0) < 1e-5

    # Min score
    score, breakdown = scorer.blend(0.0, 0.0, 0.0)
    assert abs(score - 0.0) < 1e-5

    # Mixed score
    # 0.5*0.4 + 1.0*0.4 + 0.0*0.2 = 0.2 + 0.4 + 0.0 = 0.6
    score, breakdown = scorer.blend(0.5, 1.0, 0.0)
    assert abs(score - 0.6) < 1e-5
    assert breakdown["behavior_score"] == score
