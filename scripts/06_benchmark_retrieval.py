import os
import sys
import json
import time

# Ensure backend directory is in path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(project_root, 'backend'))

from retrieval.candidate_selector import CandidateSelector
from retrieval.retrieval_metrics import MetricsTracker

JDS = [
    {
        "id": "JD_01",
        "title": "Machine Learning Engineer",
        "description": "Looking for an experienced Machine Learning Engineer with strong Python, PyTorch, and NLP skills. Experience with LLMs and prompt engineering is a huge plus. Must be able to deploy models to AWS or GCP using Docker and Kubernetes."
    },
    {
        "id": "JD_02",
        "title": "Senior Backend Developer",
        "description": "We need a Senior Backend Developer proficient in Node.js, TypeScript, and PostgreSQL. You should have experience building scalable microservices and REST APIs. Familiarity with Redis, Kafka, and Docker is required."
    },
    {
        "id": "JD_03",
        "title": "Data Scientist",
        "description": "Seeking a Data Scientist to analyze large datasets. Must know SQL, Python, pandas, scikit-learn. Experience with A/B testing and statistical modeling is required. Spark and Hadoop experience is a nice to have."
    },
    {
        "id": "JD_04",
        "title": "DevOps Engineer",
        "description": "DevOps Engineer needed to manage our cloud infrastructure on AWS. Strong skills in Terraform, Ansible, CI/CD pipelines (Jenkins, GitHub Actions), and Linux administration. Kubernetes administration is mandatory."
    },
    {
        "id": "JD_05",
        "title": "Frontend React Developer",
        "description": "Looking for a Frontend Developer with strong React, Next.js, and Tailwind CSS experience. Must understand state management (Redux, Zustand) and API integration. Experience with Framer Motion and shadcn/ui is highly preferred."
    }
]

def run_benchmark():
    cache_dir = os.path.join(project_root, "cache")
    artifacts_dir = os.path.join(project_root, "artifacts")
    os.makedirs(artifacts_dir, exist_ok=True)
    
    print("Initializing Candidate Selector (Loading FAISS, BM25, Models)...")
    init_start = time.perf_counter()
    selector = CandidateSelector(cache_dir=cache_dir)
    init_time = (time.perf_counter() - init_start) * 1000
    print(f"Initialization completed in {init_time:.2f}ms")
    
    trace_results = []
    
    for jd in JDS:
        print(f"\nProcessing {jd['title']}...")
        tracker = MetricsTracker()
        tracker.start_timer("total")
        
        candidates = selector.retrieve(jd["id"], jd["description"], metrics_tracker=tracker)
        
        tracker.stop_timer("total", "total_latency_ms")
        top_10 = candidates[:10]
        
        # We need to simulate Top-10 for FAISS and BM25 directly to satisfy "FAISS Top 10" in trace.
        # But wait, our pipeline gives hybrid scores. We can just sort the retrieved 
        # candidates by their faiss_score and bm25_score to find their local Top 10.
        
        # Sort candidates by faiss score
        faiss_top = sorted(candidates, key=lambda c: c.faiss_score, reverse=True)[:10]
        # Sort candidates by bm25 score
        bm25_top = sorted(candidates, key=lambda c: c.bm25_score, reverse=True)[:10]
        
        trace = {
            "query_id": jd["id"],
            "query_title": jd["title"],
            "execution_metrics": tracker.metrics.model_dump(),
            "faiss_top_10": [c.candidate_id for c in faiss_top],
            "bm25_top_10": [c.candidate_id for c in bm25_top],
            "hybrid_top_10": [c.candidate_id for c in top_10],
            "hybrid_top_10_scores": [{"id": c.candidate_id, "score": c.hybrid_score} for c in top_10]
        }
        trace_results.append(trace)
        
        print(f"Total Latency: {tracker.metrics.total_latency_ms:.2f}ms")
        print(f"Peak Memory: {tracker.metrics.peak_memory_mb:.2f}MB")
        print(f"FAISS/BM25 Overlap: {tracker.metrics.faiss_bm25_overlap_ratio:.2f}")

    trace_file = os.path.join(artifacts_dir, "retrieval_trace.json")
    with open(trace_file, "w") as f:
        json.dump({
            "initialization_time_ms": init_time,
            "queries": trace_results
        }, f, indent=2)
        
    print(f"\nBenchmark complete. Trace saved to {trace_file}")

if __name__ == "__main__":
    run_benchmark()
