import os
import sys
import time
import tracemalloc
from collections import Counter

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from config.settings import settings
from retrieval.candidate_selector import CandidateSelector
from intelligence.recruiter_intelligence import RecruiterIntelligenceEngine

# Mock JDs for benchmarking (from 06_benchmark_retrieval.py)
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

def run_benchmark():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    cache_dir = os.path.join(base_dir, "cache")
    artifacts_dir = os.path.join(base_dir, "artifacts")
    metadata_path = os.path.join(cache_dir, "candidate_features.parquet")
    
    if not os.path.exists(metadata_path):
        print(f"Error: {metadata_path} not found.")
        sys.exit(1)
        
    print("Initializing Candidate Selector (Retrieval)...")
    selector = CandidateSelector(cache_dir=cache_dir)
    
    print("Initializing Recruiter Intelligence Engine...")
    t0 = time.time()
    intelligence = RecruiterIntelligenceEngine(metadata_parquet_path=metadata_path)
    t1 = time.time()
    print(f"Intelligence Init Time: {(t1 - t0) * 1000:.2f}ms")
    
    tracemalloc.start()
    
    all_scores = []
    confidence_bands = []
    
    for jd in JDS:
        print(f"\nProcessing {jd['title']}...")
        
        # 1. Retrieve Hybrid
        t_ret_0 = time.time()
        retrieved_candidates = selector.retrieve(jd["id"], jd["description"])
        t_ret_1 = time.time()
        
        # 2. Intelligence Scoring
        t_int_0 = time.time()
        recruiter_candidates = intelligence.evaluate(retrieved_candidates)
        t_int_1 = time.time()
        
        print(f"Retrieval Latency: {(t_ret_1 - t_ret_0) * 1000:.2f}ms")
        print(f"Intelligence Latency: {(t_int_1 - t_int_0) * 1000:.2f}ms")
        
        # Store distribution
        for rc in recruiter_candidates:
            all_scores.append(rc.recruiter_score)
            confidence_bands.append(rc.confidence_band)
            
        # Top Candidate Summary
        if recruiter_candidates:
            top_cand = recruiter_candidates[0]
            print(f"\nTop Candidate ID: {top_cand.candidate_id}")
            print(f"Recruiter Score: {top_cand.recruiter_score:.2f} ({top_cand.confidence_band})")
            print(f"Base Score: {top_cand.base_recruiter_score:.2f}")
            print(f"Risk Multiplier: {top_cand.risk_multiplier:.2f}")
            print("Score Breakdown:")
            for k, v in top_cand.score_breakdown.items():
                print(f"  - {k}: {v:.2f}")
            print("Evidence Snippet:")
            for e in top_cand.evidence[:3]:
                print(f"  - [{e['dimension']}] {e['reason']}")

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(f"\nPeak Memory (Intelligence): {peak / 10**6:.2f}MB")
    
    # Distributions
    if all_scores:
        avg_score = sum(all_scores) / len(all_scores)
        max_score = max(all_scores)
        min_score = min(all_scores)
        print(f"\nScore Distribution over {len(all_scores)} scored candidates:")
        print(f"Average Recruiter Score: {avg_score:.2f}")
        print(f"Max Score: {max_score:.2f}")
        print(f"Min Score: {min_score:.2f}")
        
        band_counts = Counter(confidence_bands)
        print("\nConfidence Band Distribution:")
        for band, count in band_counts.most_common():
            print(f"  - {band}: {count} ({count/len(all_scores):.1%})")

if __name__ == "__main__":
    run_benchmark()
