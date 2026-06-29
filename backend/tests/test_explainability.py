import pytest
from explainability.evidence_formatter import EvidenceFormatter
from explainability.template_engine import TemplateEngine
from explainability.reason_builder import ReasonBuilder
from behavior.behavior_models import BehaviorEvidence

def test_evidence_formatter():
    formatter = EvidenceFormatter()
    
    evidence = [
        BehaviorEvidence(module="profile_quality", reason="low market validation", impact=-0.1),
        BehaviorEvidence(module="availability", reason="immediate notice period", impact=0.2)
    ]
    
    pos, neg = formatter.extract_factors(evidence)
    
    # Impact 0.2 is absolute highest, so pos should have "immediate notice period"
    # Actually wait, "immediate notice period" is mapped from "immediate notice" in our formatter
    # Let's check formatter mapping: if "immediate notice" in reason. It is.
    assert "immediate notice period" in pos[0]
    # "low market validation" -> "lower market validation"
    assert "lower market validation" in neg[0]

def test_template_engine():
    engine = TemplateEngine()
    
    # Strong all
    t_id = engine.select_template(0.8, 0.8, True, False)
    assert "strong" in t_id
    
    reason = engine.render(t_id, ["immediate notice period"], [])
    assert "immediate notice period" in reason
    assert reason[0].isupper()

def test_reason_builder():
    builder = ReasonBuilder()
    
    reason, t_id = builder.build_reason(0.9, 0.9, ["immediate availability"], ["extended notice period"])
    assert len(reason) <= 250
    assert "availability" in reason
