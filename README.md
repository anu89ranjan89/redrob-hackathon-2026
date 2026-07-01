# 🚀 Redrob Hackathon 2026 — Team MCAHeist

A production-style Python implementation of the candidate ranking pipeline developed from the feature engineering notebook.

Welcome to the official repository of **MCAHeist Team** for the Redrob Hackathon 2026. This project implements a high-performance, deterministic candidate ranking system that prioritizes matching accuracy, behavioral signal intelligence, and explainable AI.
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

### Custom Input / Output

```bash
python main.py \
  --input data/candidates.jsonl \
  --output outputs/top_candidates.csv \
  --top-n 100
```

---

## Streamlit UI & CLI System Architecture

The MCAHeist candidate ranking system is organized as a unified architecture that runs via a CLI orchestrator or a visual Streamlit web application:

```text
Job Description (JD) / Candidate Profiles
                ↓
      JD Intelligence Engine
                ↓
  Candidate Understanding Engine (Normalization)
                ↓
    Feature Engineering & Scoring
                ↓
      Honeypot/Anomaly Detector
                ↓
      Explainable Ranking Engine
                ↓
     Validated output (Top 100 Candidates)
```

1. **CLI Orchestration (`run.py`)**: Executes the entire scoring pipeline end-to-end, sorts candidates descending by final score (and ascending by ID to resolve ties), generates natural language reasonings using the explainable reasoning engine, validates constraints, and outputs the final CSV.
2. **Streamlit Application (`app.py`)**: Implements an interactive control panel dashboard ("AI Matchmaker Pro"). It invokes the CLI ranking pipeline, extracts names from candidate JSON data to merge them with scores on the fly, presents a beautiful leaderboard, and allows exporting the final leaderboard (with names) as an Excel (`.xlsx`) spreadsheet.

---

## Ranking Features Dictionary

### Technical Fit Features

* **skill_overlap_score** (Weight: 0.08): Percentage overlap between JD skills and candidate skills (Range: 0.0–1.0).
* **retrieval_score** (Weight: 0.15): Keyword-based relevance score measuring retrieval/search concepts (e.g. vector databases, embeddings, LLMs, RAG).
* **dynamic_experience_score** (Weight: 0.10): Matches years of experience dynamically against the range specified in the JD.
* **dynamic_title_score** (Weight: 0.08): Matches current title dynamically against titles specified in the JD.
* **dynamic_jd_score** (Weight: 0.20): Matches candidates' profiles using a dynamic keyword matching regex derived directly from the job description.
* **technical_production_score** (Weight: 0.10): Detects proximity matches between technical actions (e.g. built, shipped, deployed) and technical system concepts.

### Recruitability & Behavioral Features

* **behavior_score** (Weight: 0.08): Synthesizes open-to-work status, notice period (shorter notice is preferred), recruiter response rate, interview completion rate, and offer acceptance rate.
* **production_score** (Weight: 0.08): Measures overall evidence of software delivery in production.

### Activity Features

* **activity_score** (Weight: 0.08): Derived from profile recency (last active days), applications submitted, and recruiter search appearances in the last 30/90 days.

### Trust Features

* **trust_score** (Weight: 0.05): Measures profile authenticity using verification signals (verified email, phone, connected LinkedIn, and profile completeness).

---

## Final Ranking Formula

The final score integrates the engineered features using the following weights:

$$
\begin{aligned}
\text{final\_score} = & \,\, 0.10 \times \text{dynamic\_experience\_score} \\
& + 0.08 \times \text{dynamic\_title\_score} \\
& + 0.08 \times \text{behavior\_score} \\
& + 0.08 \times \text{production\_score} \\
& + 0.10 \times \text{technical\_production\_score} \\
& + 0.15 \times \text{retrieval\_score} \\
& + 0.20 \times \text{dynamic\_jd\_score} \\
& + 0.08 \times \text{activity\_score} \\
& + 0.05 \times \text{trust\_score} \\
& + 0.08 \times \text{skill\_overlap\_score}
\end{aligned}
$$

All rankings are strictly deterministic and sorted in descending order of final score. In case of ties, the system breaks ties by sorting candidate IDs in ascending order.

---

## 👥 Team MCAHeist Members

* **Anupriya Ranjan (Data):** JD Intelligence, relevance rubrics, and data processing.
* **Lakshman Kumar (Scoring):** Feature engineering, candidate scoring, and ranking engine.
* **Divyanshu Tiwari (Packaging & Reproducibility):** Pipeline assembly, validation logic, templates, and reproducibility verification.

---

Built with 💙 for the Redrob Hackathon 2026.
