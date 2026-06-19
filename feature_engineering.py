"""Feature engineering for candidate ranking."""

from __future__ import annotations

import re
from collections.abc import Sequence

import pandas as pd

from utils import career_descriptions, safe_text

# Configurable scoring constants.
STRONG_TITLE_MATCHES = {
    "Recommendation Systems Engineer",
    "Search Engineer",
    "Machine Learning Engineer",
    "Senior Machine Learning Engineer",
    "Applied ML Engineer",
    "AI Engineer",
    "Lead AI Engineer",
    "NLP Engineer",
    "Senior NLP Engineer",
    "Senior Applied Scientist",
}

MEDIUM_TITLE_MATCHES = {
    "Backend Engineer",
    "Data Engineer",
    "Software Engineer",
}

WEAK_TITLE_MATCHES = {
    "Business Analyst",
    "Project Manager",
    "Operations Manager",
}

VERY_WEAK_TITLE_MATCHES = {
    "Accountant",
    "HR Manager",
    "Marketing Manager",
    "Graphic Designer",
    "Content Writer",
    "Customer Support",
    "Mechanical Engineer",
    "Civil Engineer",
}

TITLE_SCORE_MAP = {
    **{title: 1.0 for title in STRONG_TITLE_MATCHES},
    **{title: 0.8 for title in MEDIUM_TITLE_MATCHES},
    **{title: 0.3 for title in WEAK_TITLE_MATCHES},
    **{title: 0.0 for title in VERY_WEAK_TITLE_MATCHES},
}

KEYWORD_GROUPS = {
    "retrieval_keyword_count": [
        "retrieval",
        "retrieval system",
        "retrieval systems",
        "search",
        "semantic search",
        "vector search",
        "rag",
    ],
    "embedding_keyword_count": [
        "embedding",
        "embeddings",
        "semantic matching",
        "sentence transformer",
        "sentence transformers",
        "similarity search",
    ],
    "vector_db_keyword_count": [
        "vector database",
        "vector databases",
        "vector db",
        "vector store",
        "vector stores",
        "faiss",
        "pinecone",
        "weaviate",
        "milvus",
        "chroma",
        "qdrant",
    ],
    "llm_keyword_count": [
        "llm",
        "llms",
        "large language model",
        "large language models",
        "gpt",
        "openai",
        "anthropic",
        "langchain",
        "llamaindex",
        "prompt engineering",
    ],
    "evaluation_keyword_count": [
        "evaluation",
        "evaluations",
        "eval",
        "evals",
        "benchmark",
        "benchmarks",
        "metric",
        "metrics",
        "relevance scoring",
        "ranking quality",
    ],
}

STRONG_PRODUCTION_SIGNALS = [
    "shipped",
    "deployed",
    "in production",
    "production",
    "launched",
    "owned",
    "led",
    "designed",
    "built",
]

MEDIUM_PRODUCTION_SIGNALS = [
    "implemented",
    "developed",
    "worked on",
    "created",
]

TECHNICAL_ACTIONS = [
    "built",
    "shipped",
    "deployed",
    "implemented",
    "designed",
    "developed",
]

TECHNICAL_OBJECTS = [
    "model",
    "models",
    "ranking",
    "retrieval",
    "recommendation",
    "search",
    "pipeline",
    "pipelines",
    "embeddings",
    "vector database",
    "vector db",
    "ml system",
    "machine learning",
    "feature store",
    "xgboost",
    "lightgbm",
    "spark",
    "airflow",
    "faiss",
    "pinecone",
    "qdrant",
    "elasticsearch",
]

EXPERIENCE_SCORE_DEFAULT = 0.2
OFFER_ACCEPTANCE_UNKNOWN_SCORE = 0.5

FINAL_KEYWORD_COUNT_COLUMNS = list(KEYWORD_GROUPS)
KEYWORD_PATTERNS = {
    count_column: [
        re.compile(rf"(?<!\w){re.escape(keyword)}(?!\w)", flags=re.IGNORECASE)
        for keyword in keywords
    ]
    for count_column, keywords in KEYWORD_GROUPS.items()
}
STRONG_PRODUCTION_PATTERNS = [
    re.compile(rf"(?<!\w){re.escape(signal)}(?!\w)", flags=re.IGNORECASE)
    for signal in STRONG_PRODUCTION_SIGNALS
]
MEDIUM_PRODUCTION_PATTERNS = [
    re.compile(rf"(?<!\w){re.escape(signal)}(?!\w)", flags=re.IGNORECASE)
    for signal in MEDIUM_PRODUCTION_SIGNALS
]
ACTION_PATTERN = r"(?:" + "|".join(re.escape(action) for action in TECHNICAL_ACTIONS) + r")"
OBJECT_PATTERN = r"(?:" + "|".join(re.escape(obj) for obj in TECHNICAL_OBJECTS) + r")"
NEARBY_WORDS_PATTERN = r"(?:\W+\w+){0,8}?\W+"
TECHNICAL_PRODUCTION_PATTERN = re.compile(
    rf"(?<!\w)(?:{ACTION_PATTERN}{NEARBY_WORDS_PATTERN}{OBJECT_PATTERN}|"
    rf"{OBJECT_PATTERN}{NEARBY_WORDS_PATTERN}{ACTION_PATTERN})(?!\w)",
    flags=re.IGNORECASE,
)


# Build a unified text representation for candidate matching.
def build_candidate_text(candidates: pd.DataFrame) -> pd.DataFrame:
    """Create the text field used by keyword and production scoring."""
    candidates["candidate_text"] = (
        candidates["profile_summary"].apply(safe_text)
        + " "
        + candidates["profile_headline"].apply(safe_text)
        + " "
        + candidates["career_history"].apply(career_descriptions)
    ).str.strip()
    return candidates


# Score candidate experience against the target range.
def create_experience_score(candidates: pd.DataFrame) -> pd.DataFrame:
    """Score experience against the target 5-9 year range."""
    years = candidates["profile_years_of_experience"]
    candidates["experience_score"] = EXPERIENCE_SCORE_DEFAULT
    candidates.loc[years.between(5, 9, inclusive="both"), "experience_score"] = 1.0
    candidates.loc[
        ((4 <= years) & (years < 5)) | ((9 < years) & (years <= 10)),
        "experience_score",
    ] = 0.8
    candidates.loc[
        ((3 <= years) & (years < 4)) | ((10 < years) & (years <= 12)),
        "experience_score",
    ] = 0.5
    return candidates


# Score current-title relevance from configured buckets.
def create_title_score(candidates: pd.DataFrame) -> pd.DataFrame:
    """Score current title relevance using the notebook title buckets."""
    candidates["title_score"] = candidates["profile_current_title"].map(TITLE_SCORE_MAP).fillna(0.0)
    return candidates


# Combine behavioral signals into a single score.
def create_behavior_score(candidates: pd.DataFrame) -> pd.DataFrame:
    """Create recruitability and behavioral score features."""
    candidates["open_to_work_score"] = candidates["redrob_signals_open_to_work_flag"].astype(float)
    candidates["notice_score"] = candidates["redrob_signals_notice_period_days"].apply(
        _score_notice_period
    )
    candidates["offer_acceptance_score"] = candidates[
        "redrob_signals_offer_acceptance_rate"
    ].replace(-1, OFFER_ACCEPTANCE_UNKNOWN_SCORE)

    behavior_score_columns = [
        "open_to_work_score",
        "redrob_signals_recruiter_response_rate",
        "notice_score",
        "redrob_signals_interview_completion_rate",
        "offer_acceptance_score",
    ]
    candidates["behavior_score"] = candidates[behavior_score_columns].mean(axis=1)
    return candidates


# Count retrieval keywords and normalize the weighted score.
def create_retrieval_score(candidates: pd.DataFrame) -> pd.DataFrame:
    """Create keyword-count retrieval score features."""
    keyword_counts = pd.DataFrame.from_records(
        candidates["candidate_text"].map(_count_all_keyword_groups),
        index=candidates.index,
    )
    candidates[list(KEYWORD_PATTERNS)] = keyword_counts[list(KEYWORD_PATTERNS)]

    weighted_score = (
        5 * candidates["retrieval_keyword_count"]
        + 4 * candidates["embedding_keyword_count"]
        + 4 * candidates["vector_db_keyword_count"]
        + 4 * candidates["evaluation_keyword_count"]
        + 2 * candidates["llm_keyword_count"]
    )

    candidates["total_keyword_count"] = candidates[FINAL_KEYWORD_COUNT_COLUMNS].sum(axis=1)
    max_weighted_score = weighted_score.max()
    candidates["retrieval_score"] = (
        weighted_score / max_weighted_score if max_weighted_score else 0.0
    )
    return candidates


# Score production evidence and technical production proximity.
def create_technical_production_score(candidates: pd.DataFrame) -> pd.DataFrame:
    """Create production and technical-production score features."""
    candidates = _create_production_score(candidates)

    technical_production_raw_score = candidates["candidate_text"].apply(
        _count_technical_production_phrases
    )
    max_technical_production_raw_score = technical_production_raw_score.max()
    candidates["technical_production_score"] = (
        technical_production_raw_score / max_technical_production_raw_score
        if max_technical_production_raw_score
        else 0.0
    )
    return candidates


# Score a single notice-period value.
def _score_notice_period(days: int) -> float:
    if days <= 30:
        return 1.0
    if days <= 60:
        return 0.7
    if days <= 90:
        return 0.4
    return 0.1


# Normalize generic production-signal counts.
def _create_production_score(candidates: pd.DataFrame) -> pd.DataFrame:
    production_signal_counts = pd.DataFrame.from_records(
        candidates["candidate_text"].map(_count_production_signals),
        index=candidates.index,
    )
    production_raw_score = (
        2 * production_signal_counts["strong_count"]
        + production_signal_counts["medium_count"]
    )

    max_production_raw_score = production_raw_score.max()
    candidates["production_score"] = (
        production_raw_score / max_production_raw_score if max_production_raw_score else 0.0
    )
    return candidates


# Count technical action/object proximity matches.
def _count_technical_production_phrases(text: str) -> int:
    return len(TECHNICAL_PRODUCTION_PATTERN.findall(safe_text(text)))


# Count all configured keyword groups for one candidate text.
def _count_all_keyword_groups(text: str) -> dict[str, int]:
    cleaned_text = safe_text(text)
    return {
        count_column: _count_compiled_patterns(cleaned_text, patterns)
        for count_column, patterns in KEYWORD_PATTERNS.items()
    }


# Count strong and medium production signals for one candidate text.
def _count_production_signals(text: str) -> dict[str, int]:
    cleaned_text = safe_text(text)
    return {
        "strong_count": _count_compiled_patterns(cleaned_text, STRONG_PRODUCTION_PATTERNS),
        "medium_count": _count_compiled_patterns(cleaned_text, MEDIUM_PRODUCTION_PATTERNS),
    }


# Count matches across precompiled regex patterns.
def _count_compiled_patterns(text: str, patterns: Sequence[re.Pattern[str]]) -> int:
    return sum(len(pattern.findall(text)) for pattern in patterns)
