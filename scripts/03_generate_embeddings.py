import hashlib
import json
import logging
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

import numpy as np
import polars as pl
import psutil
from sentence_transformers import SentenceTransformer
from sklearn.neighbors import NearestNeighbors  # type: ignore

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
FEATURES_PARQUET = PROJECT_ROOT / "artifacts" / "candidate_features.parquet"
OUTPUT_EMBEDDINGS = PROJECT_ROOT / "artifacts" / "candidate_embeddings.npy"
OUTPUT_METADATA_PARQUET = PROJECT_ROOT / "artifacts" / "candidate_metadata.parquet"
EMBEDDING_METADATA_JSON = PROJECT_ROOT / "artifacts" / "embedding_metadata.json"

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
BATCH_SIZE = 256


def generate_embeddings() -> None:
    if not FEATURES_PARQUET.exists():
        logger.error(f"Features file missing at {FEATURES_PARQUET}")
        sys.exit(1)

    logger.info(f"Loading {MODEL_NAME} on CPU...")
    # Using CPU explicitly to satisfy constraints and reproducibility
    model = SentenceTransformer(MODEL_NAME, device="cpu")

    logger.info("Loading feature dataset...")
    # We only need candidate_id and semantic_text
    df = pl.read_parquet(FEATURES_PARQUET, columns=["candidate_id", "semantic_text"])

    total_rows = df.height
    logger.info(f"Loaded {total_rows} rows.")

    # Save the metadata dataframe (just candidate_ids for alignment with the index)
    logger.info("Saving candidate_metadata.parquet...")
    df.select("candidate_id").write_parquet(OUTPUT_METADATA_PARQUET)

    # Convert to list of texts for streaming
    texts = df["semantic_text"].to_list()

    logger.info(f"Generating embeddings with batch size {BATCH_SIZE}...")
    start_time = time.time()

    # Normalize embeddings directly during encode
    embeddings = model.encode(
        texts,
        batch_size=BATCH_SIZE,
        show_progress_bar=True,
        normalize_embeddings=True,
        convert_to_numpy=True,
    )

    elapsed = time.time() - start_time
    logger.info(f"Completed in {elapsed:.2f} seconds.")

    peak_mem_mb = psutil.Process().memory_info().rss / (1024 * 1024)
    logger.info(f"Peak memory: {peak_mem_mb:.2f} MB")

    logger.info("Saving embeddings to NPY...")
    np.save(OUTPUT_EMBEDDINGS, embeddings)

    # Checksum
    checksum = hashlib.md5(embeddings.tobytes()).hexdigest()

    # Verification
    logger.info("Verifying embedding quality...")
    rng = np.random.default_rng(seed=42)
    sample_indices = rng.choice(total_rows, size=5, replace=False)

    nn = NearestNeighbors(n_neighbors=5, metric="cosine")
    nn.fit(embeddings)

    verification_results = []

    for idx in sample_indices:
        query_emb = embeddings[idx].reshape(1, -1)
        distances, indices = nn.kneighbors(query_emb)

        # distance in cosine metric is 1 - similarity
        similarities = 1 - distances[0]

        res: Dict[str, Any] = {
            "query_id": str(df["candidate_id"][idx]),
            "query_text_snippet": texts[idx][:100] + "...",
            "neighbors": [],
        }

        # Skip the first one since it's the query itself (similarity ~1.0)
        for i in range(1, 5):
            n_idx = indices[0][i]
            res["neighbors"].append(
                {
                    "neighbor_id": str(df["candidate_id"][n_idx]),
                    "similarity": float(similarities[i]),
                    "neighbor_text_snippet": texts[n_idx][:100] + "...",
                }
            )

        verification_results.append(res)

    logger.info("Quality Verification complete. Similarities look reasonable.")

    metadata = {
        "embedding_model": MODEL_NAME,
        "embedding_dimension": int(embeddings.shape[1]),
        "normalization_method": "L2",
        "batch_size": BATCH_SIZE,
        "runtime_seconds": round(elapsed, 2),
        "peak_memory_mb": round(peak_mem_mb, 2),
        "number_of_embeddings": total_rows,
        "checksum_md5": checksum,
        "generation_timestamp": datetime.now().isoformat(),
        "limitations": (
            "Currently only supporting a single combined 'semantic_text' view. "
            "Future updates can extend this to semantic_profile, "
            "semantic_career, and semantic_skills."
        ),
        "verification_sample": verification_results,
    }

    with open(EMBEDDING_METADATA_JSON, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    logger.info(f"Saved metadata to {EMBEDDING_METADATA_JSON}")
    logger.info("Script 3 Complete.")


if __name__ == "__main__":
    generate_embeddings()
