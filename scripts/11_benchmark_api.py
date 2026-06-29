import os
import sys
import json
import time
import tracemalloc
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from main import app

def run_benchmark():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    artifacts_dir = os.path.join(base_dir, "artifacts")
    os.makedirs(artifacts_dir, exist_ok=True)
    
    print("Initializing TestClient (Startup Phase)...")
    
    tracemalloc.start()
    
    start_time = time.time()
    
    # Context manager triggers lifespan events (init_pipeline)
    with TestClient(app) as client:
        startup_latency = time.time() - start_time
        
        print(f"Startup Time: {startup_latency*1000:.2f}ms")
        
        # 1. Health Endpoint
        health_resp = client.get("/health")
        print(f"Health check: {health_resp.status_code}")
        
        # 2. Metrics Endpoint
        metrics_resp = client.get("/metrics")
        print(f"Metrics: {metrics_resp.status_code}")
        
        # 3. End-to-End Ranking Endpoint
        jd_payload = {
            "job_id": "jd_ml_1",
            "job_description": "Looking for a Machine Learning Engineer with Python and FAISS."
        }
        
        rank_start = time.time()
        rank_resp = client.post("/api/v1/rank", json=jd_payload)
        rank_latency = time.time() - rank_start
        
        print(f"Ranking Endpoint Status: {rank_resp.status_code}")
        print(f"End-to-End API Latency: {rank_latency*1000:.2f}ms")
        
        rank_data = rank_resp.json()
        
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        print(f"Peak Memory Overhead (API test): {peak / 10**6:.2f}MB")
        
        # Output Examples
        with open(os.path.join(artifacts_dir, "endpoint_examples.json"), "w") as f:
            json.dump({
                "health_response": health_resp.json(),
                "metrics_response": metrics_resp.json(),
                "rank_response_top_2": rank_data["candidates"][:2] if "candidates" in rank_data else []
            }, f, indent=2)
            
        with open(os.path.join(artifacts_dir, "api_benchmark.json"), "w") as f:
            json.dump({
                "startup_time_ms": startup_latency * 1000,
                "end_to_end_latency_ms": rank_latency * 1000,
                "peak_memory_mb": peak / 10**6
            }, f, indent=2)

if __name__ == "__main__":
    run_benchmark()
