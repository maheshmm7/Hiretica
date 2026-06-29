import os
from typing import Optional

from core.pipeline import AIPipeline

_pipeline_instance: Optional[AIPipeline] = None


def init_pipeline():
    global _pipeline_instance
    if _pipeline_instance is None:
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        cache_dir = os.path.join(base_dir, "cache")
        _pipeline_instance = AIPipeline(cache_dir=cache_dir)


def get_pipeline() -> AIPipeline:
    global _pipeline_instance
    if _pipeline_instance is None:
        init_pipeline()
    # Ignoring mypy since it cannot know that init_pipeline initializes it
    return _pipeline_instance  # type: ignore
