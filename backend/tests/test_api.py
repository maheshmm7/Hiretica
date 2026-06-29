import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "HIRETICA API is running."}

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["version"] == "1.0.0"
    assert "pipeline" in data["components"]

def test_version():
    response = client.get("/version")
    assert response.status_code == 200
    assert response.json() == {"version": "1.0.0"}

def test_metrics():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "startup_time_ms" in response.json()

def test_rank_empty_jd():
    response = client.post("/api/v1/rank", json={
        "job_id": "test_1",
        "job_description": "   "
    })
    # FastAPI pydantic validation min_length=10 should catch this before our 400
    assert response.status_code == 422 
    
def test_rank_valid():
    # Only test a small snippet to see if it routes correctly
    response = client.post("/api/v1/rank", json={
        "job_id": "test_1",
        "job_description": "Looking for a Machine Learning Engineer with Python."
    })
    assert response.status_code == 200
    data = response.json()
    assert data["job_id"] == "test_1"
    assert "candidates" in data
    assert len(data["candidates"]) > 0

def test_explain_empty():
    response = client.post("/api/v1/explain", json={
        "candidates": []
    })
    assert response.status_code == 400
