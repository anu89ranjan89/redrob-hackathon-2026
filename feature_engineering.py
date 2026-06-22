"""Feature engineering for candidate ranking."""

from __future__ import annotations

import re
from collections.abc import Sequence
from collections import Counter
import pandas as pd

from utils import career_descriptions, safe_text
from jd_utils import (
    extract_jd_keywords,
    extract_experience_range,
    extract_jd_titles,
)
from datetime import datetime
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
# Placeholder for dynamic JD patterns (populated when dynamic JD keywords are extracted).
JD_DYNAMIC_PATTERNS: dict[str, list[re.Pattern[str]]] = {}
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
    ).str.lower().str.strip()
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


# Score current-title 
def create_title_score(
    candidates: pd.DataFrame,
    jd_text: str,
) -> pd.DataFrame:

    jd_keywords = set(
        extract_jd_keywords(jd_text)
    )

    def score(title):

        title_words = set(
            safe_text(title)
            .lower()
            .split()
        )

        overlap = len(
            jd_keywords.intersection(
                title_words
            )
        )

        if overlap >= 3:
            return 1.0

        if overlap == 2:
            return 0.8

        if overlap == 1:
            return 0.5

        return 0.0

    candidates["title_score"] = (
        candidates[
            "profile_current_title"
        ]
        .fillna("")
        .apply(score)
    )

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
def create_retrieval_score(
    candidates: pd.DataFrame
) -> pd.DataFrame:

    text_series = (
        candidates["candidate_text"]
        .str.lower()
        .fillna("")
    )

    candidates["retrieval_keyword_count"] = (
       text_series.str.count("retrieval")
       +
       text_series.str.count("search")
       +
       text_series.str.count("rag")
    )

    candidates["embedding_keyword_count"] = (
       text_series.str.count("embedding")
       +
      text_series.str.count("embeddings")
    )

    candidates["vector_db_keyword_count"] = (
       text_series.str.count("faiss")
       +
       text_series.str.count("pinecone")
       +
       text_series.str.count("qdrant")
    )

    candidates["llm_keyword_count"] = (
       text_series.str.count("llm")
        +
       text_series.str.count("gpt")
       +
       text_series.str.count("langchain")
    )

    candidates["evaluation_keyword_count"] = (
       text_series.str.count("evaluation")
       +
       text_series.str.count("benchmark")
    )

    candidates[list(KEYWORD_PATTERNS)] = candidates[
        list(KEYWORD_PATTERNS)
    ]

    weighted_score = (
        5 * candidates["retrieval_keyword_count"]
        + 4 * candidates["embedding_keyword_count"]
        + 4 * candidates["vector_db_keyword_count"]
        + 4 * candidates["evaluation_keyword_count"]
        + 2 * candidates["llm_keyword_count"]
    )

    candidates["total_keyword_count"] = (
        candidates[
            FINAL_KEYWORD_COUNT_COLUMNS
        ].sum(axis=1)
    )

    max_weighted_score = weighted_score.max()

    base_score = (
        weighted_score / max_weighted_score
        if max_weighted_score > 0
        else 0.0
    )

    # Dynamic JD retrieval contribution

    jd_keywords = set(
        extract_jd_keywords(
            candidates.attrs.get(
                "jd_text",
                ""
            )
        )
    )

    if jd_keywords:

        dynamic_count = (
            candidates["candidate_text"]
            .str.lower()
            .str.split()
            .apply(
                lambda words:
                len(
                    jd_keywords.intersection(
                        words
                    )
                )
            )
        )

        max_dynamic = dynamic_count.max()

        dynamic_score = (
            dynamic_count / max_dynamic
            if max_dynamic > 0
            else 0.0
        )

        candidates["retrieval_score"] = (
            0.5 * base_score
            +
            0.5 * dynamic_score
        )

    else:

        candidates["retrieval_score"] = (
            base_score
        )

    return candidates

def create_dynamic_jd_score(
    candidates: pd.DataFrame,
    jd_text: str,
) -> pd.DataFrame:
    """
    Fast dynamic JD matching.
    """

    jd_keywords = extract_jd_keywords(jd_text)

    if not jd_keywords:
        candidates["dynamic_jd_score"] = 0.0
        return candidates

    jd_keywords = [
        kw.lower()
        for kw in jd_keywords[:30]
    ]


    # Single regex instead of 30 regex scans
    pattern = r"\b(?:{})\b".format(
        "|".join(
            map(
                re.escape,
                jd_keywords,
            )
        )
    )

    counts = (
        candidates["candidate_text"]
        .str.lower()
        .str.count(pattern)
    )

    max_count = counts.max()

    candidates["dynamic_jd_score"] = (
        counts / max_count
        if max_count > 0
        else 0.0
    )

    return candidates



def create_dynamic_experience_score(
    candidates: pd.DataFrame,
    jd_text: str,
) -> pd.DataFrame:

    min_exp, max_exp = extract_experience_range(jd_text)

    years = candidates["profile_years_of_experience"]

    candidates["dynamic_experience_score"] = 0.2

    candidates.loc[
        years.between(min_exp, max_exp),
        "dynamic_experience_score",
    ] = 1.0

    candidates.loc[
        (
            (years >= min_exp - 1)
            & (years < min_exp)
        )
        |
        (
            (years > max_exp)
            & (years <= max_exp + 1)
        ),
        "dynamic_experience_score",
    ] = 0.8

    candidates.loc[
        (
            (years >= min_exp - 2)
            & (years < min_exp - 1)
        )
        |
        (
            (years > max_exp + 1)
            & (years <= max_exp + 3)
        ),
        "dynamic_experience_score",
    ] = 0.5

    return candidates


def create_dynamic_title_score(
    candidates: pd.DataFrame,
    jd_text: str,
) -> pd.DataFrame:

    jd_titles = extract_jd_titles(jd_text)

    if not jd_titles:
        candidates["dynamic_title_score"] = (
            candidates["title_score"]
        )
        return candidates

    def score(title):

        title = safe_text(title).lower()

        for jd_title in jd_titles:

            if jd_title == title:
                return 1.0

            if (
                jd_title in title
                or
                title in jd_title
            ):
                return 0.8

        return 0.2

    candidates["dynamic_title_score"] = (
        candidates[
            "profile_current_title"
        ].apply(score)
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
def _count_compiled_patterns(
    text,
    patterns,
) -> int:
    
    count = 0

    for pattern in patterns:

        if pattern.search(text):
            count += 1

    return count


def _count_dynamic_keywords(text: str) -> dict[str, int]:
    cleaned_text = safe_text(text)

    return {
        count_column: _count_compiled_patterns(
            cleaned_text,
            patterns,
        )
        for count_column, patterns in JD_DYNAMIC_PATTERNS.items()
    }

def create_activity_score(
    candidates: pd.DataFrame,
) -> pd.DataFrame:

    today = pd.Timestamp.today()

    last_active_days = (
        today -
        pd.to_datetime(
            candidates[
                "redrob_signals_last_active_date"
            ]
        )
    ).dt.days

    recency_score = (
        1 -
        (last_active_days / last_active_days.max())
    ).clip(0, 1)

    applications_score = (
        candidates[
            "redrob_signals_applications_submitted_30d"
        ]
        /
        candidates[
            "redrob_signals_applications_submitted_30d"
        ].max()
    ).fillna(0)

    search_score = (
        candidates[
            "redrob_signals_search_appearance_30d"
        ]
        /
        candidates[
            "redrob_signals_search_appearance_30d"
        ].max()
    ).fillna(0)

    saved_score = (
        candidates[
            "redrob_signals_saved_by_recruiters_30d"
        ]
        /
        candidates[
            "redrob_signals_saved_by_recruiters_30d"
        ].max()
    ).fillna(0)

    candidates["activity_score"] = (
        0.4 * recency_score
        + 0.2 * applications_score
        + 0.2 * search_score
        + 0.2 * saved_score
    )

    return candidates


def create_trust_score(
    candidates: pd.DataFrame,
) -> pd.DataFrame:

    candidates["trust_score"] = (

        candidates[
            "redrob_signals_verified_email"
        ].astype(float)

        +

        candidates[
            "redrob_signals_verified_phone"
        ].astype(float)

        +

        candidates[
            "redrob_signals_linkedin_connected"
        ].astype(float)

        +

        (
            candidates[
                "redrob_signals_profile_completeness_score"
            ] / 100
        )

    ) / 4

    return candidates


def create_skill_overlap_score(
    candidates: pd.DataFrame,
    jd_text: str,
) -> pd.DataFrame:

    jd_keywords = set(
        extract_jd_keywords(jd_text)
    )

    def score(skills):

        candidate_skills = {
            safe_text(
                skill.get(
                    "name",
                    ""
                )
            ).lower()

            for skill in skills
        }

        overlap = (
            jd_keywords &
            candidate_skills
        )

        if len(jd_keywords) == 0:
            return 0.0

        return (
            len(overlap)
            /
            len(jd_keywords)
        )

    candidates[
        "skill_overlap_score"
    ] = candidates[
        "skills"
    ].apply(score)

    return candidates