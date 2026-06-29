import os
import sys
import json
import time
import statistics
import tracemalloc
from collections import Counter

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from retrieval.candidate_selector import CandidateSelector
from intelligence.recruiter_intelligence import RecruiterIntelligenceEngine
from behavior.behavior_engine import BehaviorIntelligenceEngine

# Mock JDs for benchmarking
JDS = [
    {
        "id": "jd_ml_1",
        "title": "Machine Learning Engineer",
        "description": "Looking for a Machine Learning Engineer with strong Python and FAISS experience."
    },
    {
        "id": "jd_backend_1",
        "title": "Senior Backend Developer",
        "description": "Backend developer with 5+ years of experience in Python, FastAPI, and Postgres."
    },
    {
        "id": "jd_ds_1",
        "title": "Data Scientist",
        "description": "Data Scientist experienced in DuckDB, Polars, and statistical modeling."
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
    
    tracemalloc.start()
    start_time = time.time()
    behavior_engine = BehaviorIntelligenceEngine(metadata_parquet_path=metadata_path)
    init_time = time.time() - start_time
    print(f"Behavior Engine Init Time: {init_time*1000:.2f}ms")
    
    all_scores = []
    hiring_readiness = []
    behavior_flags = []
    behavior_evidence = []
    
    total_behavior_latency = 0
    
    for jd in JDS:
        print(f"\nProcessing {jd['title']}...")
        retrieved = selector.retrieve(jd["id"], jd["description"])
        recruiter_candidates = intelligence.evaluate(retrieved)
        
        t0 = time.time()
        behavior_candidates = behavior_engine.evaluate(recruiter_candidates)
        t1 = time.time()
        
        total_behavior_latency += (t1 - t0)
        
        for bc in behavior_candidates:
            all_scores.append(bc.behavior_score)
            hiring_readiness.append(bc.hiring_readiness)
            behavior_flags.extend(bc.behavior_flags)
            for ev in bc.behavior_evidence:
                behavior_evidence.append(ev.reason)
                
        # Print top candidate
        if behavior_candidates:
            top_bc = max(behavior_candidates, key=lambda x: x.behavior_score)
            print(f"Top Candidate ID: {top_bc.candidate_id}")
            print(f"Behavior Score: {top_bc.behavior_score:.2f}")
            print(f"Hiring Readiness: {top_bc.hiring_readiness}")
            print(f"Breakdown: {json.dumps(top_bc.behavior_breakdown, indent=2)}")
            print(f"Flags: {top_bc.behavior_flags}")
            
    print(f"\nTotal Behavior Evaluation Latency (750 candidates): {total_behavior_latency*1000:.2f}ms")
    
    current, peak = tracemalloc.get_traced_memory()
    print(f"Peak Memory (Behavior Engine): {peak / 10**6:.2f}MB")
    tracemalloc.stop()
    
    # Calculate stats
    if all_scores:
        stats = {
            "count": len(all_scores),
            "min": min(all_scores),
            "max": max(all_scores),
            "mean": statistics.mean(all_scores),
            "median": statistics.median(all_scores),
            "std_dev": statistics.stdev(all_scores) if len(all_scores) > 1 else 0.0,
            "histogram": generate_histogram(all_scores)
        }
        
        readiness_counts = Counter(hiring_readiness)
        readiness_dist = {
            "Highly Ready": readiness_counts.get("Highly Ready", 0),
            "Ready": readiness_counts.get("Ready", 0),
            "Passive": readiness_counts.get("Passive", 0),
            "Unlikely": readiness_counts.get("Unlikely", 0)
        }
        
        flag_counts = Counter(behavior_flags)
        evidence_counts = Counter(behavior_evidence)
        
        with open(os.path.join(artifacts_dir, "behavior_score_distribution.json"), "w") as f:
            json.dump({
                "scores": stats,
                "hiring_readiness": readiness_dist,
                "top_flags": dict(flag_counts.most_common(10)),
                "top_evidence": dict(evidence_counts.most_common(10))
            }, f, indent=2)
            
        print("\nBehavior Distribution Generated:")
        print(json.dumps(readiness_dist, indent=2))
        print("Top Flags:")
        print(json.dumps(dict(flag_counts.most_common(5)), indent=2))
        
if __name__ == "__main__":
    run_benchmark()
