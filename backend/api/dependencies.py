import logging
import os
import shutil
import urllib.request
import zipfile
from typing import Optional

from core.pipeline import AIPipeline

_pipeline_instance: Optional[AIPipeline] = None
logger = logging.getLogger(__name__)


def verify_cache_artifacts(cache_dir: str) -> bool:
    required_files = [
        "bm25.pkl",
        "candidate_embeddings.npy",
        "candidate_features.parquet",
        "candidate_metadata.parquet",
        "faiss.index",
    ]
    for filename in required_files:
        if not os.path.exists(os.path.join(cache_dir, filename)):
            return False
    return True


def ensure_cache_exists(cache_dir: str):
    if verify_cache_artifacts(cache_dir):
        return

    logger.warning("One or more required cache artifacts are missing.")

    # If not on Render, skip downloader and preserve local dev behavior
    if not os.environ.get("RENDER"):
        logger.warning("Local development detected. Skipping cache download.")
        return

    archive_url = os.environ.get("CACHE_ARCHIVE_URL")
    if not archive_url:
        raise RuntimeError(
            "Deployment Error: CACHE_ARCHIVE_URL environment variable is required to download "
            "missing cache artifacts. Please set it to a direct download URL of your cache.zip."
        )

    logger.warning(f"Downloading cache archive from {archive_url}...")
    os.makedirs(cache_dir, exist_ok=True)
    zip_path = os.path.join(cache_dir, "cache_archive.zip")

    try:
        urllib.request.urlretrieve(archive_url, zip_path)
    except Exception as e:
        raise RuntimeError(
            f"Deployment Error: Failed to download cache archive from {archive_url}: {e}"
        )

    logger.warning("Extracting cache archive...")
    try:
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(cache_dir)

        # Robustness: If user zipped the folder itself rather than contents, move them up.
        extracted_sub_cache = os.path.join(cache_dir, "cache")
        if os.path.isdir(extracted_sub_cache):
            for item in os.listdir(extracted_sub_cache):
                shutil.move(os.path.join(extracted_sub_cache, item), cache_dir)
            os.rmdir(extracted_sub_cache)

    except Exception as e:
        raise RuntimeError(
            f"Deployment Error: Failed to extract cache archive. Ensure it is a valid ZIP file: {e}"
        )
    finally:
        if os.path.exists(zip_path):
            os.remove(zip_path)

    if not verify_cache_artifacts(cache_dir):
        raise RuntimeError(
            "Deployment Error: Cache archive was extracted but required files are still missing. Verify the ZIP structure."
        )

    logger.warning("Cache artifacts successfully restored.")


def init_pipeline():
    global _pipeline_instance
    if _pipeline_instance is None:
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        cache_dir = os.path.join(base_dir, "cache")

        ensure_cache_exists(cache_dir)

        _pipeline_instance = AIPipeline(cache_dir=cache_dir)


def get_pipeline() -> AIPipeline:
    global _pipeline_instance
    if _pipeline_instance is None:
        init_pipeline()
    # Ignoring mypy since it cannot know that init_pipeline initializes it
    return _pipeline_instance  # type: ignore
