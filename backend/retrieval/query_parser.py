import re

from .retrieval_models import QueryContext


class QueryParser:
    def __init__(self):
        # A simple technical keyword regex pattern (can be extended)
        self.keyword_pattern = re.compile(r"\b([A-Za-z0-9#\+\.]+)\b")
        self.stop_words = {
            "and",
            "or",
            "the",
            "a",
            "an",
            "in",
            "on",
            "with",
            "to",
            "for",
            "of",
        }

    def parse(self, job_id: str, raw_text: str) -> QueryContext:
        """
        Parses raw JD text into a QueryContext suitable for downstream embedding and lexical matching.
        """
        # Lexical extraction (lowercase, alphanumeric, no stopwords)
        tokens = self.keyword_pattern.findall(raw_text.lower())
        lexical_query = [t for t in tokens if t not in self.stop_words and len(t) > 1]

        return QueryContext(
            job_id=job_id,
            raw_text=raw_text,
            lexical_query=lexical_query,
            semantic_embedding=None,
        )
