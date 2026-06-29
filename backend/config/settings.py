import os
import yaml
from pydantic import BaseModel, Field

class RetrievalConfig(BaseModel):
    faiss_top_n: int
    hybrid_top_k: int

class FusionConfig(BaseModel):
    alpha: float
    beta: float
    normalization: str

class IntelligenceWeights(BaseModel):
    technical_fit: float
    experience_fit: float
    career_progression: float
    leadership: float
    domain_relevance: float
    career_stability: float
    growth_trend: float

class IntelligenceConfig(BaseModel):
    weights: IntelligenceWeights

class RiskMultipliersConfig(BaseModel):
    low: float
    medium: float
    high: float
    critical: float

class ConfidenceThresholdsConfig(BaseModel):
    exceptional: float
    high: float
    medium: float

class WeightsConfig(BaseModel):
    technical_fit: float
    career_progression: float
    behavior_intelligence: float

class TechnicalDimensions(BaseModel):
    semantic_similarity: float
    keyword_match: float
    production_ai_experience: float

class CareerDimensions(BaseModel):
    experience_relevance: float
    career_stability: float

class BehaviorDimensions(BaseModel):
    recruiter_engagement: float
    candidate_availability: float
    location_compatibility: float

class DimensionsConfig(BaseModel):
    technical: TechnicalDimensions
    career: CareerDimensions
    behavior: BehaviorDimensions

class BoostsConfig(BaseModel):
    github_assessment: float
    recruiter_validation: float

class NoticePeriodPenalty(BaseModel):
    threshold_days: int
    multiplier_60_plus: float
    multiplier_90_plus: float

class InactivityPenalty(BaseModel):
    threshold_days: int
    multiplier: float

class FlakeRiskPenalty(BaseModel):
    min_completion_rate: float
    multiplier: float

class ConsultingPenalty(BaseModel):
    multiplier: float

class PenaltiesConfig(BaseModel):
    notice_period: NoticePeriodPenalty
    inactivity: InactivityPenalty
    flake_risk: FlakeRiskPenalty
    consulting_research_only: ConsultingPenalty

class ThresholdsConfig(BaseModel):
    hard_filter_max_inactive_days: int
    min_job_hopping_index: float
    max_years_experience: int

class RankingConfig(BaseModel):
    retrieval: RetrievalConfig
    fusion: FusionConfig
    intelligence: IntelligenceConfig
    risk_multipliers: RiskMultipliersConfig
    confidence_thresholds: ConfidenceThresholdsConfig
    weights: WeightsConfig
    dimensions: DimensionsConfig
    boosts: BoostsConfig
    penalties: PenaltiesConfig
    thresholds: ThresholdsConfig

def load_config(config_path: str = "config/ranking_config.yaml") -> RankingConfig:
    # Resolve relative to project root
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    full_path = os.path.join(project_root, config_path)
    
    if not os.path.exists(full_path):
        raise FileNotFoundError(f"Configuration file not found at {full_path}")
        
    with open(full_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
        
    return RankingConfig(**data)

# Singleton configuration loader
settings = load_config()
