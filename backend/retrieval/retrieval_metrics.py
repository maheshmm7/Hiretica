import time
import tracemalloc
from typing import Dict, List

from pydantic import BaseModel


class RetrievalMetrics(BaseModel):
    initialization_time_ms: float = 0.0
    faiss_latency_ms: float = 0.0
    bm25_latency_ms: float = 0.0
    fusion_latency_ms: float = 0.0
    total_latency_ms: float = 0.0
    peak_memory_mb: float = 0.0
    faiss_bm25_overlap_ratio: float = 0.0


class MetricsTracker:
    def __init__(self):
        self._start_times: Dict[str, float] = {}
        self.metrics = RetrievalMetrics()
        tracemalloc.start()

    def _get_memory_mb(self) -> float:
        current, peak = tracemalloc.get_traced_memory()
        return peak / (1024 * 1024)

    def start_timer(self, name: str):
        self._start_times[name] = time.perf_counter()

    def stop_timer(self, name: str, metric_attr: str):
        if name in self._start_times:
            elapsed = (time.perf_counter() - self._start_times[name]) * 1000.0
            setattr(self.metrics, metric_attr, elapsed)
            del self._start_times[name]

    def update_peak_memory(self):
        current_mem = self._get_memory_mb()
        if current_mem > self.metrics.peak_memory_mb:
            self.metrics.peak_memory_mb = current_mem

    def compute_overlap(self, faiss_ids: List[str], bm25_ids: List[str]):
        if not faiss_ids or not bm25_ids:
            self.metrics.faiss_bm25_overlap_ratio = 0.0
            return
        set_faiss = set(faiss_ids)
        set_bm25 = set(bm25_ids)
        intersection = len(set_faiss.intersection(set_bm25))
        union = len(set_faiss.union(set_bm25))
        self.metrics.faiss_bm25_overlap_ratio = (
            intersection / union if union > 0 else 0.0
        )
