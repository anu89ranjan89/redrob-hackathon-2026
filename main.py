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
    create_technical_production_score,
    create_title_score,
)
from ranking import create_final_score, get_top_candidates
from utils import configure_logging, load_data

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
    return parser.parse_args()


# Run feature engineering, ranking, and CSV export.
def run_pipeline(input_path: str, output_path: str, top_n: int) -> None:
    candidates = load_data(input_path)

    LOGGER.info("Building candidate text...")
    candidates = build_candidate_text(candidates)

    LOGGER.info("Calculating experience scores...")
    candidates = create_experience_score(candidates)

    LOGGER.info("Calculating title scores...")
    candidates = create_title_score(candidates)

    LOGGER.info("Calculating behavior scores...")
    candidates = create_behavior_score(candidates)

    LOGGER.info("Calculating retrieval scores...")
    candidates = create_retrieval_score(candidates)

    LOGGER.info("Calculating technical production scores...")
    candidates = create_technical_production_score(candidates)

    LOGGER.info("Calculating final scores...")
    candidates = create_final_score(candidates)

    LOGGER.info("Selecting top %s candidates...", top_n)
    top_candidates = get_top_candidates(candidates, limit=top_n)

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
        "final_score",
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

# Execute the pipeline from the CLI.
def main() -> None:
    configure_logging()
    args = parse_args()
    run_pipeline(args.input, args.output, args.top_n)


if __name__ == "__main__":
    main()
