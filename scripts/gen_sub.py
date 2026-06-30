import requests
import json
import csv

def generate_submission():
    payload = {
        "job_id": "REQ-1234",
        "job_description": "Looking for a Senior Python Developer with 5 years experience. Must have machine learning and API experience."
    }
    response = requests.post("http://127.0.0.1:8000/api/v1/workspace", json=payload)
    if response.status_code != 200:
        print("API Error:", response.text)
        return
        
    data = response.json()
    preview = data.get("submission_preview", [])
    
    with open("submission.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["candidate_id", "rank", "score", "reasoning"])
        for row in preview:
            writer.writerow([row["candidate_id"], row["rank"], row["score"], row["reasoning"]])
            
    print(f"Generated submission.csv with {len(preview)} rows.")

if __name__ == "__main__":
    generate_submission()
