import json
import logging
import sys
from pathlib import Path
from typing import Any, Dict

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATASET_PATH = PROJECT_ROOT / "dataset" / "candidates.jsonl"
SCHEMA_PATH = PROJECT_ROOT / "dataset" / "candidate_schema.json"

EXPECTED_ROW_COUNT = 100000


def load_schema_required_fields(schema_path: Path) -> Dict[str, Any]:
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    required = {
        "top_level": set(schema.get("required", [])),
        "profile": set(schema["properties"]["profile"].get("required", [])),
        "career_history": set(
            schema["properties"]["career_history"]["items"].get("required", [])
        ),
        "education": set(
            schema["properties"]["education"]["items"].get("required", [])
        ),
        "skills": set(schema["properties"]["skills"]["items"].get("required", [])),
        "redrob_signals": set(
            schema["properties"]["redrob_signals"].get("required", [])
        ),
    }
    return required


def validate_dataset():
    if not DATASET_PATH.exists():
        logger.error(f"Dataset not found at {DATASET_PATH}")
        sys.exit(1)

    if not SCHEMA_PATH.exists():
        logger.error(f"Schema not found at {SCHEMA_PATH}")
        sys.exit(1)

    required_fields = load_schema_required_fields(SCHEMA_PATH)

    total_rows = 0
    corrupted_rows = 0
    missing_fields_errors = 0

    logger.info(f"Starting validation of {DATASET_PATH}...")

    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        for line_number, line in enumerate(f, start=1):
            total_rows += 1
            if total_rows % 20000 == 0:
                logger.info(f"Processed {total_rows} rows...")

            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                corrupted_rows += 1
                logger.error(f"Row {line_number}: JSON Decode Error")
                continue

            # Check top level
            missing = required_fields["top_level"] - set(record.keys())
            if missing:
                missing_fields_errors += 1
                logger.debug(f"Row {line_number}: Missing top-level fields: {missing}")
                continue

            # Check profile
            if "profile" in record and isinstance(record["profile"], dict):
                missing = required_fields["profile"] - set(record["profile"].keys())
                if missing:
                    missing_fields_errors += 1
                    logger.debug(
                        f"Row {line_number}: Missing profile fields: {missing}"
                    )
                    continue

            # Check redrob_signals
            if "redrob_signals" in record and isinstance(
                record["redrob_signals"], dict
            ):
                missing = required_fields["redrob_signals"] - set(
                    record["redrob_signals"].keys()
                )
                if missing:
                    missing_fields_errors += 1
                    logger.debug(
                        f"Row {line_number}: Missing redrob_signals fields: {missing}"
                    )
                    continue

    logger.info("=== Validation Summary ===")
    logger.info(f"Expected Rows: {EXPECTED_ROW_COUNT}")
    logger.info(f"Actual Rows: {total_rows}")
    logger.info(f"Corrupted (Invalid JSON) Rows: {corrupted_rows}")
    logger.info(f"Missing Required Fields Errors: {missing_fields_errors}")

    if total_rows != EXPECTED_ROW_COUNT:
        logger.warning(
            f"Row count mismatch! Expected {EXPECTED_ROW_COUNT}, got {total_rows}"
        )

    if (
        corrupted_rows == 0
        and missing_fields_errors == 0
        and total_rows == EXPECTED_ROW_COUNT
    ):
        logger.info("Dataset is valid and ready for feature extraction.")
    else:
        logger.warning("Dataset validation completed with errors or warnings.")


if __name__ == "__main__":
    validate_dataset()
