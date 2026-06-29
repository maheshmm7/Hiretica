import json
import logging
import sys
from datetime import datetime
from pathlib import Path

import polars as pl
from typing import Dict, Any

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATASET_PATH = PROJECT_ROOT / "dataset" / "candidates.jsonl"
OUTPUT_PARQUET = PROJECT_ROOT / "cache" / "candidate_features.parquet"
METADATA_JSON = PROJECT_ROOT / "artifacts" / "feature_metadata.json"
STATS_JSON = PROJECT_ROOT / "artifacts" / "feature_statistics.json"

TARGET_DATE = datetime(2026, 6, 30)

CORE_SKILLS = {
    "faiss",
    "duckdb",
    "pinecone",
    "weaviate",
    "milvus",
    "qdrant",
    "sentence-transformers",
    "opensearch",
    "elasticsearch",
    "bge",
    "e5",
    "llm",
    "rag",
    "retrieval",
    "ranking",
}


def extract_features() -> None:
    if not DATASET_PATH.exists():
        logger.error(f"Dataset missing at {DATASET_PATH}")
        sys.exit(1)

    features = []
    logger.info("Starting feature extraction...")

    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        for line in f:
            record = json.loads(line)

            cand_id = record["candidate_id"]
            prof = record.get("profile", {})
            career = record.get("career_history", [])
            skills = record.get("skills", [])
            signals = record.get("redrob_signals", {})

            # --- Profile Features ---
            years_exp = float(prof.get("years_of_experience", 0.0))

            # --- Career Features ---
            total_roles = len(career)
            job_hopping_index = years_exp / total_roles if total_roles > 0 else 0.0

            production_ai_score = 0
            research_roles = 0
            semantic_career_texts = []

            for role in career:
                desc = role.get("description", "").lower()
                industry = role.get("industry", "").lower()
                title = role.get("title", "").lower()

                semantic_career_texts.append(title)

                if (
                    "research" in title
                    or "research" in desc
                    or "lab" in industry
                    or "university" in industry
                ):
                    research_roles += 1

                if (
                    "tech" in industry
                    or "software" in industry
                    or "it services" in industry
                ):
                    if (
                        "deploy" in desc
                        or "production" in desc
                        or "scale" in desc
                        or "inference" in desc
                    ):
                        production_ai_score += 1

            research_ratio = research_roles / total_roles if total_roles > 0 else 0.0

            # --- Skill Features ---
            core_skill_match_count = 0
            vector_db_experience = False
            total_proficiency = 0
            prof_map = {"beginner": 1, "intermediate": 2, "advanced": 3, "expert": 4}
            skill_names = []

            for skill in skills:
                name = skill.get("name", "").lower()
                skill_names.append(name)

                if any(cs in name for cs in CORE_SKILLS):
                    core_skill_match_count += 1

                if any(
                    vdb in name
                    for vdb in ["pinecone", "milvus", "faiss", "weaviate", "qdrant"]
                ):
                    vector_db_experience = True

                total_proficiency += prof_map.get(skill.get("proficiency", ""), 1)

            avg_skill_prof = total_proficiency / len(skills) if skills else 0.0

            # --- Behavioral Features ---
            last_active = signals.get("last_active_date")
            if last_active:
                try:
                    dt = datetime.strptime(last_active, "%Y-%m-%d")
                    days_since_active = (TARGET_DATE - dt).days
                except ValueError:
                    days_since_active = 9999
            else:
                days_since_active = 9999

            notice_period = int(signals.get("notice_period_days", 0))

            # --- Derived & Risk Features ---
            honeypot_flag = False
            if years_exp > 50:
                honeypot_flag = True

            total_duration_months = sum(r.get("duration_months", 0) for r in career)
            if total_duration_months / 12.0 > years_exp + 2:
                honeypot_flag = True

            # Semantic text for embedding
            titles = prof.get("current_title", "")
            summary = prof.get("summary", "")
            s_skills = " ".join(skill_names)
            s_career = " ".join(semantic_career_texts)
            semantic_text = f"{titles} {summary} {s_skills} {s_career}"

            features.append(
                {
                    "candidate_id": cand_id,
                    "years_of_experience": years_exp,
                    "job_hopping_index": job_hopping_index,
                    "production_ai_score": production_ai_score,
                    "research_ratio": research_ratio,
                    "core_skill_match_count": core_skill_match_count,
                    "vector_db_experience": vector_db_experience,
                    "avg_skill_proficiency": avg_skill_prof,
                    "days_since_active": days_since_active,
                    "recruiter_response_rate": float(
                        signals.get("recruiter_response_rate", 0.0)
                    ),
                    "notice_period_days": notice_period,
                    "github_activity_score": float(
                        signals.get("github_activity_score", -1.0)
                    ),
                    "interview_completion_rate": float(
                        signals.get("interview_completion_rate", 0.0)
                    ),
                    "open_to_work_flag": bool(signals.get("open_to_work_flag", False)),
                    "location": prof.get("location", ""),
                    "honeypot_flag": honeypot_flag,
                    "semantic_text": semantic_text,
                }
            )

            if len(features) % 20000 == 0:
                logger.info(f"Extracted {len(features)} records...")

    logger.info("Converting to Polars DataFrame...")
    df = pl.DataFrame(features)

    # Save Parquet
    df.write_parquet(OUTPUT_PARQUET)
    logger.info(f"Saved parquet to {OUTPUT_PARQUET}")

    # Generate metadata
    metadata = {
        "candidate_id": {
            "type": "string",
            "nullable": False,
            "description": "Unique ID",
            "category": "Candidate Profile",
        },
        "years_of_experience": {
            "type": "float",
            "nullable": False,
            "description": "Years of exp",
            "category": "Candidate Profile",
        },
        "job_hopping_index": {
            "type": "float",
            "nullable": False,
            "description": "Exp / total roles",
            "category": "Career",
        },
        "production_ai_score": {
            "type": "int",
            "nullable": False,
            "description": "Keywords in tech roles",
            "category": "Career",
        },
        "research_ratio": {
            "type": "float",
            "nullable": False,
            "description": "Research roles / total roles",
            "category": "Career",
        },
        "core_skill_match_count": {
            "type": "int",
            "nullable": False,
            "description": "JD core skills matched",
            "category": "Skills",
        },
        "vector_db_experience": {
            "type": "bool",
            "nullable": False,
            "description": "Has vector DB skills",
            "category": "Skills",
        },
        "avg_skill_proficiency": {
            "type": "float",
            "nullable": False,
            "description": "Average mapped prof",
            "category": "Skills",
        },
        "days_since_active": {
            "type": "int",
            "nullable": False,
            "description": "Days since last active",
            "category": "Behavioral",
        },
        "recruiter_response_rate": {
            "type": "float",
            "nullable": False,
            "description": "Response rate",
            "category": "Behavioral",
        },
        "notice_period_days": {
            "type": "int",
            "nullable": False,
            "description": "Notice period",
            "category": "Behavioral",
        },
        "github_activity_score": {
            "type": "float",
            "nullable": False,
            "description": "GitHub score",
            "category": "Peer",
        },
        "interview_completion_rate": {
            "type": "float",
            "nullable": False,
            "description": "Interview completion",
            "category": "Behavioral",
        },
        "open_to_work_flag": {
            "type": "bool",
            "nullable": False,
            "description": "Open to work",
            "category": "Behavioral",
        },
        "location": {
            "type": "string",
            "nullable": False,
            "description": "Location",
            "category": "Candidate Profile",
        },
        "honeypot_flag": {
            "type": "bool",
            "nullable": False,
            "description": "Detected honeypot anomalies",
            "category": "Risk",
        },
        "semantic_text": {
            "type": "string",
            "nullable": False,
            "description": "Combined text for embedding",
            "category": "Semantic",
        },
    }

    with open(METADATA_JSON, "w") as f:
        json.dump(metadata, f, indent=2)

    # Generate stats
    stats: Dict[str, Any] = {
        "row_count": df.height,
        "generation_timestamp": datetime.now().isoformat(),
        "columns": {},
    }
    columns_stat: Dict[str, Any] = {}
    for col in df.columns:
        if df[col].dtype in [pl.Float64, pl.Int64, pl.Int32]:
            columns_stat[col] = {
                "null_count": df[col].null_count(),
                "min": df[col].min(),
                "max": df[col].max(),
                "mean": df[col].mean(),
            }
        else:
            columns_stat[col] = {
                "null_count": df[col].null_count(),
                "unique_values": df[col].n_unique(),
            }

    stats["columns"] = columns_stat

    with open(STATS_JSON, "w") as f:
        json.dump(stats, f, indent=2)

    logger.info("Saved metadata and stats. Done.")


if __name__ == "__main__":
    extract_features()
