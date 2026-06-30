import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"

def test_endpoint(name, method, url, payload=None):
    print(f"\n--- Testing {name} ---")
    start = time.time()
    try:
        if method == "GET":
            r = requests.get(url, timeout=30)
        else:
            r = requests.post(url, json=payload, timeout=30)
        elapsed = time.time() - start
        print(f"Status Code: {r.status_code} ({elapsed:.3f}s)")
        if r.status_code == 200:
            try:
                data = r.json()
                if isinstance(data, list):
                    print(f"Response: List of {len(data)} items")
                    if len(data) > 0:
                        print(json.dumps(data[0], indent=2)[:300] + "...")
                else:
                    print(json.dumps(data, indent=2)[:500] + ("..." if len(json.dumps(data)) > 500 else ""))
            except:
                print("Response:", r.text[:300])
        else:
            print("Error Response:", r.text)
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    test_endpoint("Root /", "GET", f"{BASE_URL}/")
    test_endpoint("Health /health", "GET", f"{BASE_URL}/health")
    test_endpoint("Version /version", "GET", f"{BASE_URL}/version")
    test_endpoint("Config /config", "GET", f"{BASE_URL}/config")
    test_endpoint("Metrics /metrics", "GET", f"{BASE_URL}/metrics")
    
    jd_payload = {
        "job_id": "REQ-MLE",
        "job_description": "We are looking for a Machine Learning Engineer with strong Python and PyTorch experience."
    }
    
    test_endpoint("Rank /api/v1/rank", "POST", f"{BASE_URL}/api/v1/rank", payload=jd_payload)
    test_endpoint("Workspace /api/v1/workspace", "POST", f"{BASE_URL}/api/v1/workspace", payload=jd_payload)
    
    # Explain expects candidates - wait, let's look up /api/v1/explain schema
