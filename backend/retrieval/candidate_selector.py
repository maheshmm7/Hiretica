import os
from typing import List, Optional

from config.settings import settings

from .bm25_service import Bm25Service
from .embedding_service import EmbeddingService
from .faiss_service import FaissService
from .hybrid_retriever import HybridRetriever
from .query_parser import QueryParser
from .retrieval_metrics import MetricsTracker
from .retrieval_models import RetrievedCandidate


class CandidateSelector:
    def __init__(self, cache_dir: str = "../cache"):
        self.query_parser = QueryParser()
        self.embedding_service = EmbeddingService()

        faiss_path = os.path.join(cache_dir, "faiss.index")
        bm25_path = os.path.join(cache_dir, "bm25.pkl")
        metadata_path = os.path.join(cache_dir, "candidate_metadata.parquet")

        self.faiss_service = FaissService(faiss_path, metadata_path)
        self.bm25_service = Bm25Service(bm25_path, metadata_path)

        alpha = settings.fusion.alpha
        normalization = settings.fusion.normalization
        self.hybrid_retriever = HybridRetriever(
            alpha=alpha, normalization=normalization
        )

    def retrieve(
        self, job_id: str, job_description: str, metrics_tracker: Optional[MetricsTracker] = None
    ) -> List[RetrievedCandidate]:
        """
        Executes the full retrieval pipeline.
        """
        if metrics_tracker is None:
            metrics_tracker = MetricsTracker()

        faiss_top_n = settings.retrieval.faiss_top_n
        hybrid_top_k = settings.retrieval.hybrid_top_k

        metrics_tracker.update_peak_memory()

        # 1. Parse Query
        query_ctx = self.query_parser.parse(job_id, job_description)

        # 2. Embedding Generation
        query_ctx.semantic_embedding = self.embedding_service.generate_embedding(
            query_ctx.raw_text
        )

        # 3. FAISS Search
        metrics_tracker.start_timer("faiss")
        faiss_scores = self.faiss_service.search(
            query_ctx.semantic_embedding, faiss_top_n
        )
        metrics_tracker.stop_timer("faiss", "faiss_latency_ms")
        metrics_tracker.update_peak_memory()

        # 4. BM25 Search (Using FAISS candidates to reduce search space, or full search if preferred.
        # Given architecture implies scoring FAISS candidates + potentially others, we do a full search for Top N)
        metrics_tracker.start_timer("bm25")
        bm25_scores = self.bm25_service.search(query_ctx.lexical_query, faiss_top_n)
        metrics_tracker.stop_timer("bm25", "bm25_latency_ms")
        metrics_tracker.update_peak_memory()

        metrics_tracker.compute_overlap(
            list(faiss_scores.keys()), list(bm25_scores.keys())
        )

        # 5. Hybrid Merge
        metrics_tracker.start_timer("fusion")
        candidates = self.hybrid_retriever.fuse(
            faiss_scores, bm25_scores, query_ctx.lexical_query
        )
        metrics_tracker.stop_timer("fusion", "fusion_latency_ms")
        metrics_tracker.update_peak_memory()

        return candidates[:hybrid_top_k]
