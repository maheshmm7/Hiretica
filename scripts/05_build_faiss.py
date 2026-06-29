import hashlib
from pathlib import Path

import faiss  # type: ignore
import numpy as np
import polars as pl
import psutil  # type: ignore

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_EMBEDDINGS = PROJECT_ROOT / "cache" / "candidate_embeddings.npy"
FEATURES_PARQUET = PROJECT_ROOT / "cache" / "candidate_features.parquet"
FAISS_INDEX = PROJECT_ROOT / "cache" / "faiss.index"
FAISS_METADATA_JSON = PROJECT_ROOT / "artifacts" / "faiss_metadata.json"


def get_memory_mb() -> float:
    process = psutil.Process()
    return process.memory_info().rss / 1024 / 1024


def build_faiss() -> None:
    start_time = time.time()
    logger.info("Loading embeddings...")
    embeddings = np.load(OUTPUT_EMBEDDINGS)

    n_candidates, dim = embeddings.shape
    logger.info(f"Loaded {n_candidates} embeddings of dimension {dim}.")

    logger.info("Building FAISS IndexFlatIP...")
    # We use IndexFlatIP for Cosine Similarity (since vectors are L2-normalized)
    index = faiss.IndexFlatIP(dim)

    # Adding IDs requires an IDMap, but since indices are 0 to n_candidates-1,
    # we can just use the standard IndexFlatIP and map array index to candidate_id
    # later. FAISS only supports 64-bit integer IDs, so we map indices to strings
    # outside FAISS.
    index.add(embeddings)

    logger.info("Saving FAISS index...")
    faiss.write_index(index, str(FAISS_INDEX))

    end_time = time.time()
    runtime = end_time - start_time
    peak_memory = get_memory_mb()

    # Checksum of the index
    with open(FAISS_INDEX, "rb") as f:
        checksum = hashlib.md5(f.read()).hexdigest()

    logger.info(f"Completed in {runtime:.2f} seconds.")
    logger.info(f"Peak memory: {peak_memory:.2f} MB")

    logger.info("Verifying retrieval...")
    # Load candidate IDs for verification mapping
    df = pl.read_parquet(FEATURES_PARQUET, columns=["candidate_id"])
    candidate_ids = df["candidate_id"].to_list()

    # Query a few random samples
    rng = np.random.default_rng(seed=42)
    sample_indices = rng.choice(n_candidates, size=3, replace=False)

    verification_results = []

    for idx in sample_indices:
        q_start = time.time()
        query_emb = embeddings[idx].reshape(1, -1)
        # Search Top-5
        distances, indices = index.search(query_emb, 5)
        q_time = time.time() - q_start

        # Result mapping
        top_candidates = [
            {
                "neighbor_id": candidate_ids[int(neighbor_idx)],
                "similarity": float(similarity),
            }
            for neighbor_idx, similarity in zip(indices[0], distances[0])
        ]

        verification_results.append(
            {
                "query_candidate_id": candidate_ids[idx],
                "latency_seconds": q_time,
                "top_5_results": top_candidates,
            }
        )

    # Calculate average retrieval latency
    avg_latency = sum(r["latency_seconds"] for r in verification_results) / len(
        verification_results
    )

    metadata = {
        "index_type": "IndexFlatIP",
        "embedding_dimension": dim,
        "vector_count": n_candidates,
        "normalization_method": "L2",
        "build_runtime_seconds": runtime,
        "peak_memory_mb": peak_memory,
        "average_retrieval_latency_seconds": avg_latency,
        "artifact_checksum_md5": checksum,
        "verification_sample": verification_results,
    }

    with open(FAISS_METADATA_JSON, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    logger.info(f"Saved metadata to {FAISS_METADATA_JSON}")


if __name__ == "__main__":
    build_faiss()
