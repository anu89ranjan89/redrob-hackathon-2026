"""Shared helpers for loading and preparing candidate data."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import pandas as pd

LOGGER = logging.getLogger(__name__)
LOAD_CHUNK_SIZE = 10_000


# Load and flatten candidate JSONL records.
def load_data(input_path: str | Path = "data/candidates.jsonl") -> pd.DataFrame:
    """Load candidate JSONL data and flatten nested profile fields."""
    path = Path(input_path)
    LOGGER.info("Loading candidate data from %s", path)

    normalized_chunks = [
        pd.json_normalize(chunk.to_dict(orient="records"), sep="_")
        for chunk in pd.read_json(path, lines=True, chunksize=LOAD_CHUNK_SIZE)
    ]
    candidates = pd.concat(normalized_chunks, ignore_index=True)

    LOGGER.info("Loaded %s candidates with %s columns", len(candidates), len(candidates.columns))
    return candidates


# Normalize nullable values into clean strings.
def safe_text(value: Any) -> str:
    """Convert missing or non-text values into clean text."""
    if value is None:
        return ""
    if not isinstance(value, (list, dict)) and pd.isna(value):
        return ""
    return str(value).strip()


# Join career-history descriptions into one text field.
def career_descriptions(career_history: Any) -> str:
    """Extract role descriptions from a candidate career history list."""
    if not isinstance(career_history, list):
        return ""

    descriptions = [
        safe_text(role.get("description"))
        for role in career_history
        if isinstance(role, dict) and safe_text(role.get("description"))
    ]
    return " ".join(descriptions)


# Configure process-wide logging for CLI execution.
def configure_logging() -> None:
    """Configure application logging once at the CLI boundary."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    )
