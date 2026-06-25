"""CLI entry point for the candidate-ranking pipeline."""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

from feature_engineering import (
    build_candidate_text,
    create_behavior_score,
    create_experience_score,
    create_retrieval_score,
    create_dynamic_jd_score,
    create_dynamic_experience_score,
    create_dynamic_title_score,
    create_technical_production_score,
    create_title_score,
    create_activity_score,
    create_trust_score,
    create_skill_overlap_score,
    create_why_selected,
)

from ranking import create_final_score, get_top_candidates
from utils import configure_logging, load_data
import time 

LOGGER = logging.getLogger(__name__)


# Parse command-line options for the ranking pipeline.
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the candidate-ranking pipeline.")
    parser.add_argument(
        "--input",
        default="data/candidates.jsonl",
        help="Path to candidate JSONL input data.",
    )
    parser.add_argument(
        "--output",
        default="outputs/top_candidates.csv",
        help="Path for the ranked candidate CSV output.",
    )
    parser.add_argument(
        "--top-n",
        type=int,
        default=100,
        help="Number of ranked candidates to write.",
    )

    parser.add_argument(
    "--jd",
    default="jd.txt",
    help="Path to job description text file.",
    )
    return parser.parse_args()


# Run feature engineering, ranking, and CSV export.
def run_pipeline(input_path: str, output_path: str, top_n: int, jd_path: str,) -> None:
    candidates = load_data(input_path)
    start_time = time.time()

    LOGGER.info("Loading job description...")

    jd_text = Path(jd_path).read_text(
        encoding="utf-8"
    )
    candidates.attrs["jd_text"] = jd_text


    LOGGER.info(
        "Loaded JD with %s characters",
        len(jd_text),
    )

    LOGGER.info("Building candidate text...")
    candidates = build_candidate_text(candidates)

    LOGGER.info("Calculating experience scores...")
    candidates = create_experience_score(candidates)

    LOGGER.info("Calculating title scores...")
    candidates = create_title_score(candidates,jd_text,)


    LOGGER.info(
    "Calculating dynamic title scores..."
    )

    candidates = create_dynamic_title_score(
    candidates,
    jd_text,
    )

    LOGGER.info("Calculating behavior scores...")
    candidates = create_behavior_score(candidates)

    LOGGER.info("Calculating retrieval scores...")
    candidates = create_retrieval_score(candidates)

    LOGGER.info("Calculating dynamic JD scores...")
    candidates = create_dynamic_jd_score(candidates, jd_text)


    LOGGER.info(
    "Calculating dynamic experience scores..."
    )

    candidates = create_dynamic_experience_score(
        candidates,
        jd_text,
    )

    LOGGER.info("Calculating activity scores...")
    candidates = create_activity_score(candidates)

    LOGGER.info("Calculating trust scores...")
    candidates = create_trust_score(candidates)

    LOGGER.info("Calculating skill overlap scores...")
    candidates = create_skill_overlap_score(
        candidates,
        jd_text,
    )

    LOGGER.info("Calculating technical production scores...")
    candidates = create_technical_production_score(candidates)

    LOGGER.info("Calculating final scores...")
    candidates = create_final_score(candidates)

    candidates = create_why_selected(candidates)

    LOGGER.info("Selecting top %s candidates...", top_n)
    top_candidates = get_top_candidates(candidates, limit=top_n)
    top_candidates = top_candidates.round(3)

    output_columns = [
        "candidate_id",
        "profile_current_title",
        "profile_years_of_experience",
        "experience_score",
        "title_score",
        "behavior_score",
        "production_score",
        "technical_production_score",
        "retrieval_score",
        "dynamic_jd_score",
        "dynamic_experience_score",
        "activity_score",
        "trust_score",
        "skill_overlap_score",
        "why_selected",
    ]

    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    LOGGER.info("Writing results to %s...", output_file)
    top_candidates[output_columns].to_csv(output_file, index=False)

    LOGGER.info(
        "Wrote %s ranked candidates to %s",
        len(top_candidates),
        output_file,
    )

    LOGGER.info(
    "Total Runtime: %.2f minutes",
    (time.time() - start_time) / 60,
    )

# Execute the pipeline from the CLI.
def main() -> None:
    configure_logging()
    args = parse_args()
    run_pipeline(
    args.input,
    args.output,
    args.top_n,
    args.jd,
    )


if __name__ == "__main__":
    main()
