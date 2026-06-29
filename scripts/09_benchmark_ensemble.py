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

# Mock JDs for benchmarking
JDS = [
    {
        "id": "jd_ml_1",
        "title": "Machine Learning Engineer",
        "description": "Looking for a Machine Learning Engineer with strong Python and FAISS experience."
    }
]

def generate_histogram(scores, bins=10):
    if not scores:
        return {}
    min_score, max_score = 0.0, 1.0
    bin_size = (max_score - min_score) / bins
    histogram = {f"{i*bin_size:.1f}-{(i+1)*bin_size:.1f}": 0 for i in range(bins)}
    
    for score in scores:
        bin_idx = min(int(score / bin_size), bins - 1)
        key = f"{bin_idx*bin_size:.1f}-{(bin_idx+1)*bin_size:.1f}"
        histogram[key] += 1
        
    return histogram

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
    
    jd = JDS[0]
    print(f"Running deterministic benchmark for {jd['title']}...")
    
    runs = 5
    top_20_across_runs = []
    first_run_stats = {}
    
    # Store hybrid scores directly from selector
    for run in range(runs):
        print(f"Run {run+1}/{runs}...")
        
        if run == 0:
            tracemalloc.start()
            start_time = time.time()
            
        # 1. Retrieval
        retrieved = selector.retrieve(jd["id"], jd["description"])
        hybrid_scores = {c.candidate_id: c.hybrid_score for c in retrieved}
        
        # 2. Recruiter Intelligence
        recruiter_candidates = intelligence.evaluate(retrieved)
        
        # 3. Behavior Intelligence
        behavior_candidates = behavior_engine.evaluate(recruiter_candidates)
        
        # 4. Final Ensemble
        ensemble_engine = FinalEnsembleEngine(hybrid_scores)
        ranked_candidates = ensemble_engine.evaluate(behavior_candidates)
        
        if run == 0:
            latency = time.time() - start_time
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            first_run_stats['latency'] = latency
            first_run_stats['peak_memory'] = peak
            first_run_stats['ranked_candidates'] = ranked_candidates
            
        top_20_across_runs.append([rc.candidate_id for rc in ranked_candidates[:20]])
    
    # Verify Determinism
    is_stable = True
    base_top_20 = top_20_across_runs[0]
    for i in range(1, runs):
        if top_20_across_runs[i] != base_top_20:
            is_stable = False
            break
            
    print(f"\nRanking Stability (across {runs} runs): {'STABLE' if is_stable else 'UNSTABLE'}")
    
    with open(os.path.join(artifacts_dir, "ranking_stability.json"), "w") as f:
        json.dump({
            "runs": runs,
            "is_stable": is_stable,
            "top_20_run_1": base_top_20,
            "top_20_run_last": top_20_across_runs[-1]
        }, f, indent=2)
        
    # Analyze First Run Stats
    all_scores = [rc.final_hiretica_score for rc in first_run_stats['ranked_candidates']]
    top_100_scores = [rc.final_hiretica_score for rc in first_run_stats['ranked_candidates'][:100]]
    
    ensemble_dist = {
        "count": len(all_scores),
        "mean": statistics.mean(all_scores),
        "median": statistics.median(all_scores),
        "max": max(all_scores),
        "min": min(all_scores),
        "histogram": generate_histogram(all_scores)
    }
    
    top_100_dist = {
        "count": len(top_100_scores),
        "mean": statistics.mean(top_100_scores),
        "median": statistics.median(top_100_scores),
        "max": max(top_100_scores),
        "min": min(top_100_scores),
    }
    
    with open(os.path.join(artifacts_dir, "ensemble_distribution.json"), "w") as f:
        json.dump({
            "overall_distribution": ensemble_dist,
            "top_100_distribution": top_100_dist,
            "latency_seconds": first_run_stats['latency'],
            "peak_memory_mb": first_run_stats['peak_memory'] / 10**6
        }, f, indent=2)
        
    print(f"\nPipeline Latency (Top 250 end-to-end): {first_run_stats['latency']*1000:.2f}ms")
    print(f"Peak Memory: {first_run_stats['peak_memory'] / 10**6:.2f}MB")
    print(f"\nOverall Average Score: {ensemble_dist['mean']:.3f}")
    print(f"Top 100 Average Score: {top_100_dist['mean']:.3f}")
    
    print("\nTop Candidate Breakdown:")
    top_cand = first_run_stats['ranked_candidates'][0]
    print(json.dumps({
        "id": top_cand.candidate_id,
        "score": top_cand.final_hiretica_score,
        "breakdown": top_cand.ranking_breakdown
    }, indent=2))
        
if __name__ == "__main__":
    run_benchmark()
