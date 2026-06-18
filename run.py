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

    # 1. Print status messages and load input files
    print(f"[STATUS] Processing job description file: '{args.jd}'")
    if os.path.exists(args.jd):
        with open(args.jd, "r", encoding="utf-8") as f:
            jd_content = f.read()
        print(f"[STATUS] Successfully read JD ({len(jd_content)} characters).")
    else:
        print(
            f"[WARNING] JD file '{args.jd}' not found. Proceeding with mock description."
        )

    print(f"[STATUS] Processing candidate data file: '{args.input}'")
    candidates = []
    if os.path.exists(args.input):
        try:
            with open(args.input, "r", encoding="utf-8") as f:
                candidates = json.load(f)
            print(
                f"[STATUS] Successfully loaded {len(candidates)} candidates from JSON."
            )
        except Exception as e:
            print(
                f"[ERROR] Failed to parse candidates JSON: {e}", file=sys.stderr
            )
            sys.exit(1)
    else:
        print(
            f"[WARNING] Candidates file '{args.input}' not found. Generating entirely synthetic candidates."
        )

    # 2. Generate mock Pandas DataFrame of 100 candidates
    print("[STATUS] Generating ranked candidate database...")

    used_candidates = []

    for i in range(100):
        # Use candidate data from JSON if available, otherwise generate mock data
        if i < len(candidates):
            cand = candidates[i]
            cid = cand.get("candidate_id")

            profile = cand.get("profile", {})
            signals = cand.get("redrob_signals", {})

            features = {
                "years_of_experience": profile.get("years_of_experience"),
                "current_title": profile.get("current_title"),
                "profile_completeness_score": signals.get(
                    "profile_completeness_score"
                ),
                "recruiter_response_rate": signals.get(
                    "recruiter_response_rate"
                ),
                "willing_to_relocate": signals.get("willing_to_relocate"),
                "github_activity_score": signals.get("github_activity_score"),
            }
        else:
            cid = f"CAND_{i+1:07d}"
            features = {
                "years_of_experience": round(random.uniform(2.0, 15.0), 1),
                "current_title": random.choice(
                    ["Backend Engineer", "ML Engineer", "HR Manager"]
                ),
                "profile_completeness_score": round(
                    random.uniform(50.0, 100.0), 1
                ),
                "recruiter_response_rate": round(random.uniform(0.1, 0.9), 2),
                "willing_to_relocate": random.choice([True, False]),
                "github_activity_score": random.randint(0, 100),
            }

        used_candidates.append((cid, features))

    candidate_ids = [item[0] for item in used_candidates]
    ranks = list(range(1, 101))

    # Generate scores strictly sorted in descending order (monotonic decreasing)
    scores = [1.0 - i * 0.008 for i in range(1, 101)]

    # 3. Apply the reasoning generator to populate a reasoning column
    reasoning_list = []
    for cid, features in used_candidates:
        reasoning_text = generate_reasoning(features)
        reasoning_list.append(reasoning_text)

    # Build the final DataFrame
    df = pd.DataFrame(
        {
            "candidate_id": candidate_ids,
            "rank": ranks,
            "score": scores,
            "reasoning": reasoning_list,
        }
    )

    # 4. Call validate_submission(df) on the final DataFrame
    print("[STATUS] Running validate_submission on final DataFrame...")
    try:
        validate_submission(df)
    except AssertionError as e:
        print(f"[ERROR] DataFrame validation failed:\n{e}", file=sys.stderr)
        sys.exit(1)

    # 5. Export to the path specified by --output (ensure directory exists)
    output_path = args.output
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        print(f"[STATUS] Ensured output directory '{output_dir}' exists.")

    df.to_csv(output_path, index=False)
    print(f"[STATUS] Pipeline run SUCCESS. Output saved to: '{output_path}'")


if __name__ == "__main__":
    main()
