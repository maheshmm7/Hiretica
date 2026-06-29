import os
import sys
import json
import statistics
import math
from collections import Counter

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from retrieval.candidate_selector import CandidateSelector
from intelligence.recruiter_intelligence import RecruiterIntelligenceEngine

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

def run_calibration():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    cache_dir = os.path.join(base_dir, "cache")
    metadata_path = os.path.join(cache_dir, "candidate_features.parquet")
    artifacts_dir = os.path.join(base_dir, "artifacts")
    
    os.makedirs(artifacts_dir, exist_ok=True)
    
    selector = CandidateSelector(cache_dir=cache_dir)
    intelligence = RecruiterIntelligenceEngine(metadata_parquet_path=metadata_path)
    
    all_scores = []
    confidence_bands = []
    
    for jd in JDS:
        retrieved_candidates = selector.retrieve(jd["id"], jd["description"])
        recruiter_candidates = intelligence.evaluate(retrieved_candidates)
        
        for rc in recruiter_candidates:
            all_scores.append(rc.recruiter_score)
            confidence_bands.append(rc.confidence_band)
            
    # Calculate statistics
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
        
        band_counts = Counter(confidence_bands)
        bands_dist = {
            "Exceptional": band_counts.get("Exceptional", 0),
            "High": band_counts.get("High", 0),
            "Medium": band_counts.get("Medium", 0),
            "Low": band_counts.get("Low", 0)
        }
        
        with open(os.path.join(artifacts_dir, "recruiter_score_distribution.json"), "w") as f:
            json.dump(stats, f, indent=2)
            
        with open(os.path.join(artifacts_dir, "confidence_distribution.json"), "w") as f:
            json.dump(bands_dist, f, indent=2)
            
        print("Calibration statistics generated.")
        print(json.dumps(stats, indent=2))
        print(json.dumps(bands_dist, indent=2))
    else:
        print("No candidates scored.")

if __name__ == "__main__":
    run_calibration()
