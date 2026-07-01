"""
reasoning.py

This module provides rule-based natural language explanation generation for candidate rankings.
It uses a pre-compiled Jinja2 template aligned with official Redrob signals.
"""

from typing import Dict, Any
import jinja2

EXPLANATION_TEMPLATE_STR = """Candidate demonstrates strong alignment for the AI/ML position with a retrieval relevance score of {{ "%.2f"|format(retrieval_score) if retrieval_score is defined and retrieval_score is not none else "0.00" }} and an experience score of {{ "%.2f"|format(experience_score) if experience_score is defined and experience_score is not none else "0.00" }}. Their technical production score of {{ "%.2f"|format(technical_production_score) if technical_production_score is defined and technical_production_score is not none else "0.00" }} and behavior score of {{ "%.2f"|format(behavior_score) if behavior_score is defined and behavior_score is not none else "0.00" }} further validate their suitability."""

EXPLANATION_TEMPLATE = jinja2.Template(EXPLANATION_TEMPLATE_STR)
REASONING_TEMPLATE_STR = EXPLANATION_TEMPLATE_STR
REASONING_TEMPLATE = EXPLANATION_TEMPLATE


class ReasoningGenerator:
    """
    ReasoningGenerator compiles the Jinja2 template once and provides a method
    to generate natural language explanations for candidate features.
    """

    @staticmethod
    def generate(candidate_features: Dict[str, Any]) -> str:
        """
        Generates a 1-2 sentence explanation for why a candidate was ranked highly
        based on their features.

        Parameters:
            candidate_features (dict): Dictionary containing candidate profile info
                                       and redrob_signals.

        Returns:
            str: A clean, formatted explanation string.
        """
        features = candidate_features or {}
        return REASONING_TEMPLATE.render(**features).strip()


def generate_reasoning(candidate_features: Dict[str, Any]) -> str:
    """
    Convenience function wrapper around ReasoningGenerator.generate.

    Parameters:
        candidate_features (dict): Candidate attributes.

    Returns:
        str: Explanation string.
    """
    return ReasoningGenerator.generate(candidate_features)
