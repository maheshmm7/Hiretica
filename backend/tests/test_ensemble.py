import pytest

from config.settings import EnsembleConfig
from ensemble.ensemble_scorer import EnsembleScorer


def test_ensemble_scorer():
    config = EnsembleConfig(
        hybrid_retrieval=0.2, recruiter_score=0.5, behavior_score=0.3
    )
    scorer = EnsembleScorer(config)

    score, breakdown = scorer.blend(1.0, 1.0, 1.0)
    assert abs(score - 1.0) < 1e-5

    score, breakdown = scorer.blend(0.5, 0.5, 0.5)
    assert abs(score - 0.5) < 1e-5

    score, breakdown = scorer.blend(1.0, 0.0, 0.0)
    assert abs(score - 0.2) < 1e-5
    assert breakdown["hybrid_contribution"] == 0.2
    assert breakdown["recruiter_contribution"] == 0.0
