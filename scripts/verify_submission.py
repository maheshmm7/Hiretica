import csv
import sys

def verify_submission(filepath: str):
    print(f"Verifying {filepath}...")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            headers = next(reader)
            
            # Check headers
            expected_headers = ["candidate_id", "rank", "score", "reasoning"]
            if headers != expected_headers:
                print(f"ERROR: Invalid headers. Expected {expected_headers}, got {headers}")
                return False
            else:
                print("Headers OK")
            
            rows = list(reader)
            if len(rows) != 100:
                print(f"WARNING: Expected 100 rows, got {len(rows)}")
            else:
                print("Row count OK (100)")
            
            prev_score = float('inf')
            seen_ids = set()
            
            for i, row in enumerate(rows):
                if len(row) != 4:
                    print(f"ERROR: Row {i+1} has {len(row)} columns, expected 4")
                    return False
                
                cid, rank, score_str, reasoning = row
                
                if cid in seen_ids:
                    print(f"ERROR: Duplicate candidate_id {cid} at rank {rank}")
                    return False
                seen_ids.add(cid)
                
                if int(rank) != i + 1:
                    print(f"ERROR: Rank mismatch. Expected {i+1}, got {rank}")
                    return False
                
                score = float(score_str)
                if score > prev_score:
                    print(f"ERROR: Scores not monotonically decreasing. Row {i+1} score {score} > prev {prev_score}")
                    return False
                prev_score = score
                
                if not reasoning.strip():
                    print(f"ERROR: Empty reasoning at rank {rank}")
                    return False
            
            print("Validation successful!")
            return True
    except Exception as e:
        print(f"Validation failed: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        verify_submission(sys.argv[1])
    else:
        print("Usage: python verify_submission.py <path_to_csv>")
