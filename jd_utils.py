"""Utilities for dynamic JD parsing."""

from __future__ import annotations

import re


STOPWORDS = {
    "the",
    "and",
    "for",
    "with",
    "that",
    "this",
    "from",
    "have",
    "has",
    "will",
    "are",
    "you",
    "your",
    "their",
    "they",
    "into",
    "about",
    "than",
    "them",
    "role",
    "candidate",
    "experience",
    "years",
    "engineering",
    "engineer",
}


def extract_jd_keywords(jd_text: str) -> list[str]:
    """
    Extract useful keywords from any JD.
    """

    words = re.findall(
        r"[a-zA-Z][a-zA-Z0-9\-\+\.#]*",
        jd_text.lower(),
    )

    keywords = []

    for word in words:
        if len(word) < 4:
            continue

        if word in STOPWORDS:
            continue

        keywords.append(word)

    return list(set(keywords))


def extract_experience_range(jd_text: str) -> tuple[int, int]:
    """
    Extract experience range from JD.
    Examples:
    5-8 years
    3 to 6 years
    4+ years
    """

    import re

    text = jd_text.lower()

    patterns = [
        r"(\d+)\s*[-to]+\s*(\d+)\s*years",
        r"(\d+)\+\s*years",
    ]

    for pattern in patterns:
        match = re.search(pattern, text)

        if match:

            if len(match.groups()) == 2:
                return (
                    int(match.group(1)),
                    int(match.group(2)),
                )

            if len(match.groups()) == 1:
                value = int(match.group(1))
                return (
                    value,
                    value + 3,
                )

    return (5, 9)

def extract_jd_titles(jd_text: str) -> list[str]:

    common_titles = [
        "machine learning engineer",
        "ml engineer",
        "ai engineer",
        "data scientist",
        "data engineer",
        "backend engineer",
        "software engineer",
        "search engineer",
        "recommendation systems engineer",
        "nlp engineer",
        "applied scientist",
        "computer vision engineer",
    ]

    text = jd_text.lower()

    matches = []

    for title in common_titles:
        if title in text:
            matches.append(title)

    return matches