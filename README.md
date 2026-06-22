# 🚀 Redrob Hackathon 2026 — Team MCA_Heist
# Redrob Hackathon 2026 – Candidate Ranking System

A production-style Python implementation of the candidate ranking pipeline developed from the feature engineering notebook.

Welcome to the official repository of **MCA_Heist Team** for the Redrob Hackathon 2026. This project implements a high-performance, deterministic candidate ranking system that prioritizes matching accuracy, behavioral signal intelligence, and explainable AI.
The system processes candidate profiles, engineers ranking features, computes relevance scores, and produces a ranked list of candidates for AI/ML-focused roles.

---

## Project Structure

```text
.
├── app.py
├── main.py
├── feature_engineering.py
├── ranking.py
├── utils.py
├── requirements.txt
├── README.md
│
├── data/
│   ├── candidate.jsonl
│   ├── candidates.jsonl
│   ├── candidate_schema.json
│   ├── jd.txt
│   ├── sample_candidates.json
│   └── ...
│
├── outputs/
│   ├── top_candidates.csv
│   └── submission.csv
│
├── notebooks/
│   ├── feature_engineering.ipynb
│   ├── evaluation.ipynb
│   └── ...
│
├── docs/
│   ├── feature_dictionary.md
│   ├── scoring_examples.md
│   ├── system_architecture.md
│   └── ...
│
├── scripts/
│   ├── pipeline.py
│   ├── validate.py
│   └── ...
│
└── venv/
```

---

## Components

### `feature_engineering.py`

Generates all ranking features:

- Candidate text construction
- Experience scoring
- Title relevance scoring
- Behavioral scoring
- Retrieval keyword scoring
- Production signal scoring
- Technical production scoring

### `ranking.py`

Responsible for:

- Final score calculation
- Candidate ranking
- Top-N candidate selection

### `utils.py`

Shared utilities:

- JSONL loading
- Logging configuration
- Text cleaning
- Career history extraction

### `main.py`

Pipeline entry point that:

1. Loads candidate data
2. Creates engineered features
3. Computes final scores
4. Produces ranked candidate output

---

## Installation

Create and activate the virtual environment:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Pipeline

Default run:

```bash
python main.py
```

This will:

- Read: `data/candidate.jsonl`
- Generate: `outputs/top_candidates.csv`

---

### Custom Input / Output

```bash
python main.py \
  --input data/candidates.jsonl \
  --output outputs/top_candidates.csv \
  --top-n 100
```

---

## Ranking Features

### Experience Score

Targets candidates with approximately 5–9 years of experience.

### Title Score

Scores current job titles based on relevance to:

- Recommendation Systems
- Search
- Machine Learning
- AI Engineering
- Data Engineering
- Backend Engineering

### Behavior Score

Combines:

- Open-to-work status
- Recruiter response rate
- Notice period
- Interview completion rate
- Offer acceptance rate

### Retrieval Score

Keyword-based relevance score using:

- Retrieval systems
- Search systems
- Embeddings
- Vector databases
- LLM tooling
- Evaluation frameworks

### Production Score

Measures evidence of real-world delivery using signals such as:

- Built
- Shipped
- Deployed
- Led
- Designed

### Technical Production Score

Measures technical production experience by identifying technical actions occurring near technical system concepts.

Examples:

- Built retrieval system
- Designed ranking model
- Shipped recommendation pipeline

---

## 👥 Team MCA_Heist Members
* **Anupriya Ranjan (Data):** JD Intelligence, relevance rubrics, and data processing.
* **Lakshman Kumar (Scoring):** Feature engineering, candidate scoring, and ranking engine.
* **Divyanshu Tiwari (Packaging & Reproducibility):** Pipeline assembly, validation logic, templates, and reproducibility verification.

---
Built with 💙 for the Redrob Hackathon 2026.
=======
## Final Ranking Formula

The final score preserves the notebook scoring logic:

```text
0.20 × experience_score
+ 0.20 × title_score
+ 0.10 × behavior_score
+ 0.10 × production_score
+ 0.15 × technical_production_score
+ 0.25 × retrieval_score
```

No ranking weights or business rules were modified during the Python refactor.

---

## Output

The pipeline generates:

```text
outputs/top_candidates.csv
```

Columns include:

- candidate_id
- profile_current_title
- profile_years_of_experience
- experience_score
- title_score
- behavior_score
- production_score
- technical_production_score
- retrieval_score
- final_score

---

## Performance

Tested on datasets containing approximately 100,000 candidate profiles.

Optimizations include:

- Reduced DataFrame copying
- Precompiled regular expressions
- Vectorized Pandas operations where possible
- Lower memory overhead during feature generation

---

## Notes

This implementation is a direct refactor of the notebook workflow into a maintainable production-style pipeline while preserving the original ranking behavior.
