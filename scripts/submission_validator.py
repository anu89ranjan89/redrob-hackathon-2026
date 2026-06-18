import pandas as pd


def validate_submission(file_path):

    df = pd.read_csv(file_path)

    print("Checking submission...")

    assert len(df) == 100, \
        "Submission must contain exactly 100 candidates."

    assert df["candidate_id"].is_unique, \
        "Duplicate candidate IDs found."

    assert df["rank"].is_unique, \
        "Duplicate ranks found."

    assert df["score"].is_monotonic_decreasing, \
        "Scores are not sorted."

    print("Submission validation passed.")


if __name__ == "__main__":

    validate_submission("../data/submission.csv")