import json
import logging
import pickle
import time
from datetime import datetime
from pathlib import Path

import psutil  # type: ignore
from rank_bm25 import BM25Okapi  # type: ignore

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATASET = PROJECT_ROOT / "dataset" / "candidates.jsonl"
OUTPUT_BM25 = PROJECT_ROOT / "cache" / "bm25.pkl"
BM25_METADATA_JSON = PROJECT_ROOT / "artifacts" / "bm25_metadata.json"


def get_memory_mb() -> float:
    process = psutil.Process()
    return process.memory_info().rss / 1024 / 1024


def build_bm25() -> None:
    start_time = time.time()
    logger.info("Streaming raw dataset to extract lexical text...")

    tokenized_corpus = []
    candidate_ids = []

    with open(RAW_DATASET, "r", encoding="utf-8") as f:
        for line in f:
            record = json.loads(line)
            candidate_id = record.get("candidate_id", "")

            profile = record.get("profile", {})
            title = profile.get("current_title", "") or ""

            experience = record.get("career_history", []) or []
            past_titles = " ".join(
                [exp.get("title", "") for exp in experience if exp.get("title")]
            )

            skills_list = record.get("skills", []) or []
            skills = " ".join([s.get("name", "") for s in skills_list if s.get("name")])

            cert_list = record.get("certifications", []) or []
            certifications = " ".join(
                [c.get("name", "") for c in cert_list if c.get("name")]
            )

            # Construct lexical text optimized for BM25
            lexical_text = f"{title} {past_titles} {skills} {certifications}"

            tokenized_corpus.append(lexical_text.lower().split())
            candidate_ids.append(candidate_id)

    total_rows = len(candidate_ids)
    logger.info(f"Loaded and tokenized {total_rows} rows.")

    logger.info("Building BM25 index...")
    bm25 = BM25Okapi(tokenized_corpus)

    logger.info("Saving BM25 index...")
    with open(OUTPUT_BM25, "wb") as f:
        pickle.dump(bm25, f)

    end_time = time.time()
    runtime = end_time - start_time
    peak_memory = get_memory_mb()

    logger.info(f"Completed in {runtime:.2f} seconds.")
    logger.info(f"Peak memory: {peak_memory:.2f} MB")

    logger.info("Verifying retrieval latency...")
    test_queries = [
        "content writer",
        "hr manager",
        "data engineer python spark",
        "software engineer java aws",
    ]

    verification_results = []

    for q in test_queries:
        q_start = time.time()
        tokenized_query = q.lower().split()
        top_n_ids = bm25.get_top_n(tokenized_query, candidate_ids, n=5)
        q_time = time.time() - q_start

        verification_results.append(
            {
                "query": q,
                "latency_seconds": q_time,
                "top_5_candidates": top_n_ids,
            }
        )

    metadata = {
        "tokenizer_strategy": "whitespace_lowercase",
        "vocabulary_size": len(bm25.idf),
        "average_document_length": float(bm25.avgdl),
        "runtime_seconds": runtime,
        "peak_memory_mb": peak_memory,
        "generation_timestamp": datetime.now().isoformat(),
        "verification_sample": verification_results,
    }

    with open(BM25_METADATA_JSON, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    logger.info(f"Saved metadata to {BM25_METADATA_JSON}")


if __name__ == "__main__":
    build_bm25()
