import os
import subprocess
import sys
import pandas as pd
import streamlit as st
from datetime import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Matchmaker Pro",
    page_icon="🚀",
    layout="wide",
)

# ---------------- CUSTOM CSS ----------------
st.markdown(
    """
<style>
    .stApp {
        background: linear-gradient(135deg, #F7F7F5 0%, #EFEFEA 100%);
        color: #1f1f1f;
    }

    #MainMenu, footer, header {visibility: hidden;}

    /* HERO HEADER */
    .hero {
        text-align: center;
        padding: 2rem 1rem;
        background: linear-gradient(90deg, #111, #333);
        color: white;
        border-radius: 14px;
        margin-bottom: 1.5rem;
    }

    .hero h1 {
        margin-bottom: 0.3rem;
        font-size: 2.2rem;
    }

    .hero p {
        opacity: 0.8;
        font-size: 1rem;
    }

    /* CARDS */
    .card {
        background: white;
        padding: 1.2rem;
        border-radius: 12px;
        border: 1px solid #e8e8e8;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        transition: transform 0.2s ease;
        height: 100%;
    }

    .card:hover {
        transform: translateY(-3px);
    }

    .card-title {
        font-weight: 600;
        margin-bottom: 0.3rem;
        font-size: 1rem;
    }

    /* METRICS */
    .metric-box {
        background: white;
        padding: 1rem;
        border-radius: 12px;
        text-align: center;
        border: 1px solid #eaeaea;
        box-shadow: 0 1px 5px rgba(0,0,0,0.05);
    }

    .metric-value {
        font-size: 1.4rem;
        font-weight: 700;
    }

    /* BUTTON */
    .stButton>button {
        background: linear-gradient(90deg, #111, #444);
        color: white;
        border-radius: 10px;
        height: 3rem;
        font-size: 1.05rem;
        border: none;
        transition: all 0.2s ease;
    }

    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }

</style>
""",
    unsafe_allow_html=True,
)

# ---------------- SIDEBAR ----------------
st.sidebar.title("⚙️ Control Panel")
st.sidebar.markdown("Configure pipeline execution")

show_logs = st.sidebar.toggle("Show Execution Logs", value=True)
show_reasoning = st.sidebar.toggle("Show Candidate Reasoning", value=True)

st.sidebar.markdown("---")
st.sidebar.info("AI Matchmaker Pro v2.0 — Hackathon Build")

# ---------------- HERO ----------------
st.markdown(
    f"""
<div class="hero">
    <h1>🚀 AI Matchmaker Pro</h1>
    <p>Hybrid AI Ranking Engine for Candidate Evaluation • Hackathon Team MCA Heist</p>
    <small>Last run: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</small>
</div>
""",
    unsafe_allow_html=True,
)

# ---------------- PIPELINE STEPS ----------------
st.subheader("🧠 System Pipeline")

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class="card">
        <div class="card-title">📥 Input Processing</div>
        Loads JD + JSON profiles and extracts structured features.
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="card">
        <div class="card-title">⚙️ Hybrid Scoring Engine</div>
        Computes weighted match score using technical + behavioral signals.
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="card">
        <div class="card-title">📊 Ranking & Validation</div>
        Produces deterministic ranking with explainable reasoning.
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ---------------- RUN BUTTON ----------------
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    run_clicked = st.button("▶ Run AI Ranking Pipeline", use_container_width=True)

# ---------------- EXECUTION ----------------
if run_clicked:

    progress = st.progress(0)
    status = st.empty()

    status.info("Initializing pipeline...")
    progress.progress(10)

    cmd = [
        sys.executable,
        "run.py",
        "--jd", "data/jd.txt",
        "--input", "data/sample_candidates.json",
        "--output", "outputs/submission.csv",
    ]

    status.info("Running scoring engine...")
    progress.progress(40)

    result = subprocess.run(cmd, capture_output=True, text=True)

    progress.progress(80)
    status.info("Processing output...")

    if result.returncode == 0:
        csv_path = "outputs/submission.csv"

        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)

            progress.progress(100)
            status.success("Pipeline executed successfully 🎉")

            st.markdown("## 📊 Key Insights")

            m1, m2, m3 = st.columns(3)

            with m1:
                st.markdown(f"""
                <div class="metric-box">
                    <div>Total Candidates</div>
                    <div class="metric-value">{len(df)}</div>
                </div>
                """, unsafe_allow_html=True)

            with m2:
                st.markdown(f"""
                <div class="metric-box">
                    <div>Max Score</div>
                    <div class="metric-value">{df['score'].max():.3f}</div>
                </div>
                """, unsafe_allow_html=True)

            with m3:
                st.markdown(f"""
                <div class="metric-box">
                    <div>Min Score</div>
                    <div class="metric-value">{df['score'].min():.3f}</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("---")

            st.subheader("🏆 Candidate Leaderboard")

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "candidate_id": "Candidate ID",
                    "rank": st.column_config.NumberColumn("Rank"),
                    "score": st.column_config.NumberColumn("Score", format="%.3f"),
                    "reasoning": st.column_config.TextColumn("AI Reasoning"),
                },
            )

            # ---------------- DETAILS SECTION ----------------
            if show_reasoning:
                st.markdown("### 🧾 Deep Dive Insights")

                for i, row in df.head(5).iterrows():
                    with st.expander(f"Candidate {row['candidate_id']} — Score {row['score']:.3f}"):
                        st.write(row.get("reasoning", "No reasoning available"))

            if show_logs:
                st.markdown("### 🖥 Execution Logs")
                st.code(result.stdout)

        else:
            st.error("Output file not found: outputs/submission.csv")

    else:
        progress.progress(100)
        st.error("Pipeline execution failed ❌")
        st.code(result.stderr)

else:
    st.info("Click the button above to run the AI ranking pipeline and generate results.")