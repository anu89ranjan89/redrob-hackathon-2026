"""
reasoning.py

This module provides rule-based natural language explanation generation for candidate rankings.
It uses a pre-compiled Jinja2 template aligned with official Redrob signals.
"""

from typing import Dict, Any

# Define the Jinja2 Template once at the module level for performance
REASONING_TEMPLATE_STR = """The candidate
{%- if years_of_experience is defined and years_of_experience is not none -%}
  , with {{ years_of_experience }} years of experience
  {%- if current_title is defined and current_title is not none -%}
    {{ ' ' }}as a {{ current_title }}
  {%- endif -%}
{%- elif current_title is defined and current_title is not none -%}
  , working as a {{ current_title }}
{%- endif -%}
{%- if profile_completeness_score is defined and profile_completeness_score is not none -%}
  , has a profile completeness score of {{ profile_completeness_score }}%
{%- elif not (years_of_experience is defined and years_of_experience is not none) and not (current_title is defined and current_title is not none) -%}
  {{ ' ' }}demonstrates strong technical capabilities
{%- endif -%}.
{%- set has_reply = recruiter_response_rate is defined and recruiter_response_rate is not none -%}
{%- set has_reloc = willing_to_relocate is defined and willing_to_relocate is not none and willing_to_relocate == true -%}
{%- set has_github = github_activity_score is defined and github_activity_score is not none and github_activity_score >= 0 -%}
{%- if has_reply or has_reloc or has_github -%}
  {{ ' ' }}They
  {%- if has_reply -%}
    {{ ' ' }}have a recruiter response rate of {{ (recruiter_response_rate * 100)|round(0)|int }}%
  {%- endif -%}
  {%- if has_github -%}
    {%- if has_reply -%}
      {{ ' ' }}and a GitHub activity score of {{ github_activity_score }}
    {%- else -%}
      {{ ' ' }}have a GitHub activity score of {{ github_activity_score }}
    {%- endif -%}
  {%- endif -%}
  {%- if has_reloc -%}
    {%- if has_reply or has_github -%}
      , and are willing to relocate
    {%- else -%}
      {{ ' ' }}are willing to relocate
    {%- endif -%}
  {%- endif -%}.
{%- endif -%}"""

import jinja2

REASONING_TEMPLATE = jinja2.Template(REASONING_TEMPLATE_STR)


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
