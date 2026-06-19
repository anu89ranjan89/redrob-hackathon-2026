# 🚀 Redrob Hackathon 2026 — Team MCA_Heist

## AI-Powered Candidate Ranking System

Welcome to the official repository of **MCA_Heist Team** for the Redrob Hackathon 2026. This project implements a high-performance, deterministic candidate ranking system that prioritizes matching accuracy, behavioral signal intelligence, and explainable AI.

---

## ⚡ Quick Start

### 1. Environment Setup
Install the required packages in your Python environment:
```bash
pip install -r requirements.txt
```

### 2. Run Pipeline Command
To run the candidate ranking pipeline end-to-end, execute the following command at the root directory:
```bash
python run.py --jd data/jd.txt --input data/sample_candidates.json --output outputs/submission.csv
```
This script runs the full ranking pipeline, generates the output, validates it against official rules, and exports it to `outputs/submission.csv`.

---

## 🏗️ Architecture & Pipeline

Our candidate discovery and ranking system follows a robust **3-step pipeline** built for speed and explainability:

### Step 1: Input Parsing
* Loads candidate datasets from JSON arrays (using the official candidate profile and Redrob signals schemas).
* Parses job description requirements from target text files.

### Step 2: Hybrid Feature Scoring
* Computes multi-dimensional matches across:
  * **Technical Fit (50%)**: Skill overlap, proficiency duration, and experience duration matching.
  * **Recruitability (25%)**: Candidate response rates, availability timeline, and notice periods.
  * **Activity (15%)**: Recent recruiter profile views, applications, and search appearances.
  * **Trust (10%)**: Email/phone verification status, profile completeness, and LinkedIn connectivity.
* Scores are normalized and sorted non-increasingly by rank. In the event of a score tie, candidate IDs are sorted in ascending order (`CAND_XXXXXXX` alphabetical sort) to satisfy the challenge tie-breaker rules.

### Step 3: Deterministic Reasoning & Output Validation
* **Rule-Based Reasoning:** Utilizes a pre-compiled Jinja2 template at the module level to generate a 1-2 sentence human-readable explanation for each candidate's rank. This method uses official Redrob behavioral signals (`profile_completeness_score`, `recruiter_response_rate`, `willing_to_relocate`, and `github_activity_score`) to produce natural, fluent text summaries without LLM hallucination risks.
* **Strict Validation:** Automatically validates the output using `validate_submission(df)` to ensure that columns, row count (exactly 100), candidate ID formats, rank order, and score monotonicity perfectly comply with the challenge specifications.

---

## ⚙️ Compliance & Reproducibility

* **100% CPU Only:** The pipeline runs completely on standard CPU environments with no GPU/TPU requirements, making it highly resource-friendly.
* **Guaranteed Determinism:** All random states are constrained using fixed seeds (`random_seed: 42`), ensuring that every run yields identical results.
* **Zero Hallucination Explanations:** Explanations are strictly fact-based and generated using rule-based Jinja2 templates instead of stochastic LLM APIs, preventing any hallucination and keeping runtime to milliseconds.
* **Zero Network Calls:** No external network requests are made during pipeline execution, fully complying with compute isolation guidelines.

---

## 👥 Team Alpha Members
* **Anupriya Ranjan (Data):** JD Intelligence, relevance rubrics, and data processing.
* **Lakshman Kumar (Scoring):** Feature engineering, candidate scoring, and ranking engine.
* **Divyanshu Tiwari (Packaging & Reproducibility):** Pipeline assembly, validation logic, templates, and reproducibility verification.

---
Built with 💙 for the Redrob Hackathon 2026.
