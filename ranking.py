"""Ranking utilities for engineered candidate features."""

from __future__ import annotations

import pandas as pd

FINAL_SCORE_WEIGHTS = {
    "experience_score": 0.20,
    "title_score": 0.20,
    "behavior_score": 0.10,
    "production_score": 0.10,
    "technical_production_score": 0.15,
    "retrieval_score": 0.25,
}


# Combine engineered features into the final score.
def create_final_score(candidates: pd.DataFrame) -> pd.DataFrame:
    """Create the final notebook v2 score without changing its weights."""
    candidates["final_score"] = sum(
        weight * candidates[column] for column, weight in FINAL_SCORE_WEIGHTS.items()
    )
    return candidates


# Select top candidates using final-score order.
def get_top_candidates(candidates: pd.DataFrame, limit: int = 100) -> pd.DataFrame:
    """Return top candidates using the notebook's final-score ordering."""
    return candidates.sort_values("final_score", ascending=False).head(limit)
