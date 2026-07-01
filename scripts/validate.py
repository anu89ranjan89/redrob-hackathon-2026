#!/usr/bin/env python3
"""
validate.py

This module contains the validate_submission(df) function to strictly verify
a hackathon submission according to the official validation rules.
"""

import re
import sys
import numpy as np
import pandas as pd

REQUIRED_HEADER = ["candidate_id", "rank", "score", "reasoning"]
CANDIDATE_ID_PATTERN = re.compile(r"^CAND_[0-9]{7}$")
EXPECTED_DATA_ROWS = 100


def validate_submission(df: pd.DataFrame, expected_rows: int = 100) -> None:
    """
    Strictly validates a hackathon submission DataFrame against official constraints.

    Checks performed:
    1. Exact column names and ordering: candidate_id, rank, score, reasoning.
    2. Exactly expected_rows rows.
    3. candidate_id matches CAND_XXXXXXX (7 digits) and values are unique.
    4. rank values are integers 1 to expected_rows and appear exactly once.
    5. score is a numeric float type.
    6. score values are non-increasing by rank (monotonic decreasing).
    7. Tie-breaker rule: if adjacent ranks have equal scores, candidate_id must be in ascending order.

    Parameters:
        df (pd.DataFrame): Submission DataFrame to validate.
        expected_rows (int): Expected number of data rows.

    Raises:
        AssertionError: If any of the constraints are violated, detailing all failures.
    """
    errors = []

    # 1. Column names and order check
    actual_cols = list(df.columns)
    if actual_cols != REQUIRED_HEADER:
        errors.append(
            "Row 1 (header) must be exactly:\n"
            f"  {','.join(REQUIRED_HEADER)}\n"
            f"Found:\n"
            f"  {','.join(actual_cols)}"
        )

    # 2. Row count check
    n = len(df)
    if n != expected_rows:
        errors.append(
            f"After the header (row 1), there must be exactly {expected_rows} "
            f"data rows; found {n}."
        )

    seen_ids = set()
    seen_ranks = set()
    by_rank = []

    # 3. Row-by-row checks
    for i in range(n):
        row_num = 2 + i  # row number corresponding to 1-indexed CSV line

        cid_val = (
            df["candidate_id"].iloc[i] if "candidate_id" in df.columns else None
        )
        rank_val = df["rank"].iloc[i] if "rank" in df.columns else None
        score_val = df["score"].iloc[i] if "score" in df.columns else None

        # Check candidate_id
        cid = None
        if cid_val is None or pd.isna(cid_val):
            errors.append(f"Row {row_num}: candidate_id is required.")
        else:
            cid = str(cid_val).strip()
            if not cid:
                errors.append(f"Row {row_num}: candidate_id is required.")
            elif not CANDIDATE_ID_PATTERN.match(cid):
                errors.append(
                    f"Row {row_num}: candidate_id must be CAND_XXXXXXX (7 digits)."
                )
            elif cid in seen_ids:
                errors.append(f"Row {row_num}: duplicate candidate_id '{cid}'.")
            else:
                seen_ids.add(cid)

        # Check rank
        rank = None
        if rank_val is None or pd.isna(rank_val):
            errors.append(f"Row {row_num}: rank must be an integer (1–{expected_rows}).")
        else:
            try:
                # To match type checks and handle float representation (e.g. 1.0)
                if isinstance(rank_val, float):
                    if not rank_val.is_integer():
                        raise ValueError
                    rank_int = int(rank_val)
                else:
                    rank_int = int(rank_val)

                if not 1 <= rank_int <= expected_rows:
                    errors.append(
                        f"Row {row_num}: rank must be between 1 and {expected_rows}."
                    )
                elif rank_int in seen_ranks:
                    errors.append(f"Row {row_num}: duplicate rank {rank_int}.")
                else:
                    seen_ranks.add(rank_int)
                    rank = rank_int
            except (ValueError, TypeError, OverflowError):
                errors.append(
                    f"Row {row_num}: rank must be an integer (1–{expected_rows})."
                )

        # Check score
        score = None
        if score_val is None or pd.isna(score_val):
            errors.append(f"Row {row_num}: score must be a float.")
        else:
            try:
                score = float(score_val)
            except (ValueError, TypeError):
                errors.append(f"Row {row_num}: score must be a float.")

        if rank is not None and score is not None and cid:
            by_rank.append((rank, score, cid))

    # 4. Rank completeness check
    missing = set(range(1, expected_rows + 1)) - seen_ranks
    if missing:
        errors.append(
            f"Each rank 1–{expected_rows} must appear exactly once; missing: {sorted(list(missing))}"
        )

    # 5. Non-increasing score by rank order checks
    by_rank.sort(key=lambda x: x[0])

    for i in range(len(by_rank) - 1):
        r1, s1, _ = by_rank[i]
        r2, s2, _ = by_rank[i + 1]
        if s1 < s2:
            errors.append(
                f"score must be non-increasing by rank: "
                f"rank {r1} ({s1}) < rank {r2} ({s2})."
            )

    # 6. Tie-breaker check (equal score requires candidate_id ascending)
    for i in range(len(by_rank) - 1):
        r1, s1, c1 = by_rank[i]
        r2, s2, c2 = by_rank[i + 1]
        if s1 == s2 and c1 > c2:
            errors.append(
                f"Equal scores at ranks {r1} and {r2}: "
                f"tie-break requires candidate_id ascending "
                f"({c1!r} > {c2!r})."
            )

    if errors:
        raise AssertionError("Validation failed:\n" + "\n".join(errors))

    print("Submission is valid.")


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python validate.py <participant_id>.csv")
        sys.exit(1)

    try:
        df = pd.read_csv(sys.argv[1])
    except FileNotFoundError:
        print(f"Error: File not found at '{sys.argv[1]}'", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file '{sys.argv[1]}': {e}", file=sys.stderr)
        sys.exit(1)

    try:
        validate_submission(df)
        print("Submission is valid.")
    except AssertionError as e:
        print(f"{e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
