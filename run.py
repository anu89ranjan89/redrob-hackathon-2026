#!/usr/bin/env python3
"""
run.py

Main CLI entry point for the candidate ranking pipeline.
Ties together the validation logic and reasoning generation.
"""

import argparse
import json
import os
import random
import sys
import numpy as np
import pandas as pd

from scripts.validate import validate_submission
from scripts.reasoning import generate_reasoning
from feature_engineering import (
    build_candidate_text,
    create_experience_score,
    create_title_score,
    create_dynamic_title_score,
    create_behavior_score,
    create_retrieval_score,
    create_dynamic_jd_score,
    create_dynamic_experience_score,
    create_activity_score,
    create_trust_score,
    create_skill_overlap_score,
    create_technical_production_score,
    create_why_selected,
)
from ranking import create_final_score


def set_seeds(seed: int = 42) -> None:
    """
    Sets seeds for random and numpy to guarantee determinism.
    """
    random.seed(seed)
    np.random.seed(seed)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Main CLI entry point for the candidate ranking pipeline."
    )
    parser.add_argument(
        "--jd",
        type=str,
        required=True,
        help="Path to job description text file."
    )
    parser.add_argument(
        "--input",
        type=str,
        required=True,
        help="Path to candidates JSON file (array of candidate objects)."
    )
    parser.add_argument(
        "--output",
        type=str,
        default="outputs/submission.csv",
        help="Path to save the final CSV (default: outputs/submission.csv)."
    )
    args = parser.parse_args()

    # Set seeds for reproducibility
    set_seeds()

    # 1. Load job description file
    print(f"[STATUS] Processing job description file: '{args.jd}'")
    jd_content = ""
    if os.path.exists(args.jd):
        with open(args.jd, "r", encoding="utf-8") as f:
            jd_content = f.read()
        print(f"[STATUS] Successfully read JD ({len(jd_content)} characters).")
    else:
        print(
            f"[WARNING] JD file '{args.jd}' not found. Proceeding with mock description."
        )
        jd_content = "Looking for a Machine Learning Engineer with 5+ years of experience in search, retrieval systems, vector databases, LLMs, and evaluation."

    # 2. Load candidate data file
    print(f"[STATUS] Processing candidate data file: '{args.input}'")
    candidates_raw = []
    if os.path.exists(args.input):
        try:
            with open(args.input, "r", encoding="utf-8") as f:
                candidates_raw = json.load(f)
            print(
                f"[STATUS] Successfully loaded {len(candidates_raw)} candidates from JSON."
            )
        except Exception as e:
            print(
                f"[ERROR] Failed to parse candidates JSON: {e}", file=sys.stderr
            )
            sys.exit(1)
    else:
        print(
            f"[ERROR] Candidates file '{args.input}' not found. Cannot proceed.", file=sys.stderr
        )
        sys.exit(1)

    # 3. Parse candidates supportively using pd.json_normalize
    print("[STATUS] Parsing and normalizing candidate JSON data...")
    candidates = pd.json_normalize(candidates_raw, sep="_")

    # Handle missing columns by pre-populating with safe defaults
    required_cols = {
        "profile_summary": "",
        "profile_headline": "",
        "profile_years_of_experience": 0.0,
        "profile_current_title": "",
        "redrob_signals_open_to_work_flag": False,
        "redrob_signals_notice_period_days": 90,
        "redrob_signals_offer_acceptance_rate": -1,
        "redrob_signals_recruiter_response_rate": 0.0,
        "redrob_signals_interview_completion_rate": 0.0,
        "redrob_signals_last_active_date": "2026-01-01",
        "redrob_signals_applications_submitted_30d": 0,
        "redrob_signals_search_appearance_30d": 0,
        "redrob_signals_saved_by_recruiters_30d": 0,
        "redrob_signals_verified_email": False,
        "redrob_signals_verified_phone": False,
        "redrob_signals_linkedin_connected": False,
        "redrob_signals_profile_completeness_score": 0.0,
    }
    for col, default_val in required_cols.items():
        if col not in candidates.columns:
            candidates[col] = default_val
        else:
            candidates[col] = candidates[col].fillna(default_val)

    if "skills" not in candidates.columns:
        candidates["skills"] = [[] for _ in range(len(candidates))]
    else:
        candidates["skills"] = candidates["skills"].apply(lambda x: x if isinstance(x, list) else [])

    if "career_history" not in candidates.columns:
        candidates["career_history"] = [[] for _ in range(len(candidates))]
    else:
        candidates["career_history"] = candidates["career_history"].apply(lambda x: x if isinstance(x, list) else [])

    # Set jd_text attribute for keyword matching
    candidates.attrs["jd_text"] = jd_content

    # 4. Run the full ML scoring pipeline
    print("[STATUS] Executing ML feature engineering and scoring pipeline...")
    candidates = build_candidate_text(candidates)
    candidates = create_experience_score(candidates)
    candidates = create_title_score(candidates, jd_content)
    candidates = create_dynamic_title_score(candidates, jd_content)
    candidates = create_behavior_score(candidates)
    candidates = create_retrieval_score(candidates)
    candidates = create_dynamic_jd_score(candidates, jd_content)
    candidates = create_dynamic_experience_score(candidates, jd_content)
    candidates = create_activity_score(candidates)
    candidates = create_trust_score(candidates)
    candidates = create_skill_overlap_score(candidates, jd_content)
    candidates = create_technical_production_score(candidates)
    candidates = create_final_score(candidates)
    candidates = create_why_selected(candidates)

    # 5. Sort candidates (descending by score, ascending by candidate_id for tie-breaking)
    print("[STATUS] Ranking candidates and applying tie-breaker rules...")
    candidates = candidates.sort_values(
        by=["final_score", "candidate_id"],
        ascending=[False, True]
    ).reset_index(drop=True)

    # 6. Select the top candidates (up to 100)
    limit = min(100, len(candidates))
    top_candidates = candidates.head(limit).copy()
    top_candidates["rank"] = range(1, limit + 1)
    top_candidates["score"] = top_candidates["final_score"]

    # 7. Generate reasoning only for the selected top candidates
    print(f"[STATUS] Generating explainable reasoning for top {limit} candidates...")
    reasonings = []
    for _, row in top_candidates.iterrows():
        features = row.to_dict()
        reasonings.append(generate_reasoning(features))
    top_candidates["reasoning"] = reasonings

    # 8. Format the final output to strictly contain candidate_id, rank, score, reasoning
    df_final = top_candidates[["candidate_id", "rank", "score", "reasoning"]].copy()

    # 9. Call validate_submission(df_final, expected_rows=limit)
    print(f"[STATUS] Validating final ranked candidate submission (expected_rows={limit})...")
    try:
        validate_submission(df_final, expected_rows=limit)
    except AssertionError as e:
        print(f"[ERROR] DataFrame validation failed:\n{e}", file=sys.stderr)
        sys.exit(1)

    # 10. Export to specified output path
    output_path = args.output
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        print(f"[STATUS] Ensured output directory '{output_dir}' exists.")

    df_final.to_csv(output_path, index=False)
    print(f"[STATUS] Pipeline run SUCCESS. Output saved to: '{output_path}'")


if __name__ == "__main__":
    main()
