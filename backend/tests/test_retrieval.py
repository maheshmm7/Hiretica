import os
import sys

import pytest

# Ensure backend directory is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from retrieval.hybrid_retriever import HybridRetriever
from retrieval.query_parser import QueryParser
from retrieval.retrieval_models import RetrievedCandidate


def test_query_parser():
    parser = QueryParser()
    ctx = parser.parse(
        "JD_01",
        "Looking for a Senior Python Developer with AWS and Kubernetes experience.",
    )
    assert ctx.job_id == "JD_01"
    assert "python" in ctx.lexical_query
    assert "aws" in ctx.lexical_query
    assert "kubernetes" in ctx.lexical_query


def test_hybrid_merge_minmax():
    import math

    retriever = HybridRetriever(alpha=0.6, normalization="minmax")

    faiss_scores = {"C1": 0.9, "C2": 0.8, "C3": 0.5}
    bm25_scores = {"C1": 15.0, "C2": 10.0, "C3": 5.0}

    candidates = retriever.fuse(faiss_scores, bm25_scores, ["python"])

    assert len(candidates) == 3
    assert candidates[0].candidate_id == "C1"

    # Calculate expected C2 score manually
    # Faiss MinMax: C1=1.0, C2=0.75, C3=0.0
    # BM25 Log1p MinMax:
    log_b1 = math.log1p(15.0)
    log_b2 = math.log1p(10.0)
    log_b3 = math.log1p(5.0)

    min_b = min(log_b1, log_b2, log_b3)
    max_b = max(log_b1, log_b2, log_b3)
    norm_b2 = (log_b2 - min_b) / (max_b - min_b)

    expected_c2_hybrid = (0.6 * 0.75) + (0.4 * norm_b2)

    assert candidates[0].hybrid_score == pytest.approx(1.0)
    assert candidates[1].candidate_id == "C2"
    assert candidates[1].hybrid_score == pytest.approx(expected_c2_hybrid)
    assert candidates[2].candidate_id == "C3"
    assert candidates[2].hybrid_score == pytest.approx(0.0)


def test_hybrid_merge_deduplication():
    retriever = HybridRetriever(alpha=0.5, normalization="minmax")

    faiss_scores = {"C1": 0.9, "C2": 0.8}
    bm25_scores = {"C2": 10.0, "C3": 5.0}

    candidates = retriever.fuse(faiss_scores, bm25_scores, ["python"])

    assert len(candidates) == 3
    # C1 only in FAISS (faiss norm=1.0, bm25 norm=0.0) -> hybrid = 0.5(1.0) + 0.5(0.0) = 0.5
    # C2 in both (faiss norm=0.0, bm25 norm=1.0) -> hybrid = 0.5(0.0) + 0.5(1.0) = 0.5
    # C3 only in BM25 (faiss norm=0.0, bm25 norm=0.0) -> hybrid = 0.0

    c1 = next(c for c in candidates if c.candidate_id == "C1")
    c2 = next(c for c in candidates if c.candidate_id == "C2")
    c3 = next(c for c in candidates if c.candidate_id == "C3")

    assert c1.retrieval_source == "faiss"
    assert c3.retrieval_source == "bm25"
    assert c2.retrieval_source == "hybrid"
