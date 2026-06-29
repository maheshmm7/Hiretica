import os
import sys
import json
import time
import tracemalloc
import statistics
from collections import Counter

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from retrieval.candidate_selector import CandidateSelector
from intelligence.recruiter_intelligence import RecruiterIntelligenceEngine
from behavior.behavior_engine import BehaviorIntelligenceEngine
from ensemble.ensemble_engine import FinalEnsembleEngine
from explainability.explainability_engine import ExplainabilityEngine

JDS = [
    {
        "id": "jd_ml_1",
        "title": "Machine Learning Engineer",
        "description": "Looking for a Machine Learning Engineer with strong Python and FAISS experience."
    }
]

def run_benchmark():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    cache_dir = os.path.join(base_dir, "cache")
    artifacts_dir = os.path.join(base_dir, "artifacts")
    metadata_path = os.path.join(cache_dir, "candidate_features.parquet")
    
    os.makedirs(artifacts_dir, exist_ok=True)
    
    print("Initializing Engines...")
    selector = CandidateSelector(cache_dir=cache_dir)
    intelligence = RecruiterIntelligenceEngine(metadata_parquet_path=metadata_path)
    behavior_engine = BehaviorIntelligenceEngine(metadata_parquet_path=metadata_path)
    explainability = ExplainabilityEngine()
    
    jd = JDS[0]
    print(f"Processing candidate explanations for {jd['title']}...")
    
    tracemalloc.start()
    
    # Run prior pipeline
    retrieved = selector.retrieve(jd["id"], jd["description"])
    hybrid_scores = {c.candidate_id: c.hybrid_score for c in retrieved}
    recruiter_candidates = intelligence.evaluate(retrieved)
    behavior_candidates = behavior_engine.evaluate(recruiter_candidates)
    ensemble_engine = FinalEnsembleEngine(hybrid_scores)
    ranked_candidates = ensemble_engine.evaluate(behavior_candidates)
    
    # Start explainability benchmark
    start_time = time.time()
    
    explained_candidates = explainability.evaluate(ranked_candidates)
    
    latency = time.time() - start_time
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    # Calculate metrics
    lengths = [ec.explanation_metadata.generated_length for ec in explained_candidates]
    templates_used = [ec.explanation_metadata.template_id for ec in explained_candidates]
    reasoning_texts = [ec.reasoning for ec in explained_candidates]
    
    avg_length = statistics.mean(lengths)
    max_length = max(lengths)
    uniqueness_rate = len(set(reasoning_texts)) / len(reasoning_texts)
    template_freq = dict(Counter(templates_used))
    
    print(f"\nExplainability Latency (Top 250): {latency*1000:.2f}ms")
    print(f"Peak Memory Overhead: {peak / 10**6:.2f}MB")
    print(f"Average Length: {avg_length:.1f} chars (Max: {max_length})")
    print(f"Uniqueness Rate: {uniqueness_rate*100:.1f}%")
    print("\nTemplate Usage:")
    for t, count in template_freq.items():
        print(f"  {t}: {count}")
        
    # Save examples for different tiers
    examples = {
        "top_10": [
            {"rank": ec.rank, "candidate_id": ec.candidate_id, "score": ec.score, "reasoning": ec.reasoning}
            for ec in explained_candidates[:10]
        ],
        "middle_50_60": [
            {"rank": ec.rank, "candidate_id": ec.candidate_id, "score": ec.score, "reasoning": ec.reasoning}
            for ec in explained_candidates[50:60]
        ],
        "bottom_240_250": [
            {"rank": ec.rank, "candidate_id": ec.candidate_id, "score": ec.score, "reasoning": ec.reasoning}
            for ec in explained_candidates[240:250]
        ]
    }
    
    with open(os.path.join(artifacts_dir, "explanation_examples.json"), "w") as f:
        json.dump(examples, f, indent=2)
        
if __name__ == "__main__":
    run_benchmark()
