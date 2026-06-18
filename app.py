import os
import subprocess
import sys
import pandas as pd
import streamlit as st

# Page configuration with target icon and wide layout
st.set_page_config(
    page_title="AI Matchmaker Sandbox",
    page_icon="📊",
    layout="wide",
)

# Custom CSS for a professional, clean SaaS aesthetic
st.markdown(
    """
<style>
    /* Background and global text color */
    .stApp {
        background-color: #F7F7F5 !important;
        color: #2B2B2B !important;
    }
    
    /* Hide default Streamlit branding elements */
    #MainMenu {
        visibility: hidden;
    }
    footer {
        visibility: hidden;
    }
    .stDeployButton {
        display: none;
    }
    
    /* Font family overrides for clean look */
    h1, h2, h3, h4, h5, h6, p, span, div, label {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
    }
    h1, h2, h3 {
        color: #111111 !important;
        font-weight: 600 !important;
    }
    
    /* Premium button styles */
    .stButton>button {
        border-radius: 6px !important;
        font-weight: 500 !important;
        border: 1px solid #D1D1D1 !important;
        background-color: #FFFFFF !important;
        color: #111111 !important;
        transition: all 0.2s ease-in-out !important;
        height: 3rem;
        font-size: 1.1em;
    }
    .stButton>button:hover {
        border-color: #888888 !important;
        background-color: #FAFAFA !important;
        box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.05) !important;
    }
    
    /* Layout card enhancements */
    .step-card {
        background-color: #FFFFFF;
        border-left: 4px solid #111111;
        padding: 1.2rem;
        border-radius: 4px;
        margin-bottom: 1rem;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        border-top: 1px solid #E5E7EB;
        border-right: 1px solid #E5E7EB;
        border-bottom: 1px solid #E5E7EB;
    }
    .step-title {
        font-weight: 600;
        color: #111111;
        margin-bottom: 0.25rem;
        font-size: 1rem;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    
    /* Hide broken material icons in expanders */
    [data-testid="stExpander"] summary span.material-symbols-rounded,
    [data-testid="stExpander"] summary span.material-icons,
    [data-testid="stExpander"] summary svg {
        display: none !important;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Centered Main Title and Subtitle without emojis
st.markdown("<h1 style='text-align: center;'>AI Matchmaker Sandbox</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.1em; color: #555; margin-bottom: 2rem;'>An interactive candidate ranking dashboard for Hackathon Team Alpha</p>", unsafe_allow_html=True)

st.subheader("System Pipeline Architecture")
col_step1, col_step2, col_step3 = st.columns(3)

with col_step1:
    st.markdown(
        """
    <div class="step-card">
        <div class="step-title">1. Input Parsing & Loading</div>
        Loads job descriptions (.txt) and candidate profiles (.json) to extract requirements and official Redrob behavioral signals.
    </div>
    """,
        unsafe_allow_html=True,
    )

with col_step2:
    st.markdown(
        """
    <div class="step-card">
        <div class="step-title">2. Hybrid Scoring Engine</div>
        Calculates matches across Technical Fit (50%), Recruitability (25%), Activity (15%), and profile Trust (10%).
    </div>
    """,
        unsafe_allow_html=True,
    )

with col_step3:
    st.markdown(
        """
    <div class="step-card">
        <div class="step-title">3. Reasoning & Validation</div>
        Uses rule-based templates for zero-hallucination explanations and validates outputs strictly against challenge specs.
    </div>
    """,
        unsafe_allow_html=True,
    )

st.markdown("---")

# Centered Run Button (search engine style layout)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    run_clicked = st.button("Run Ranking Pipeline", use_container_width=True, type="primary")

if run_clicked:
    st.markdown("<br>", unsafe_allow_html=True)
    with st.spinner("Executing deterministic pipeline on CPU..."):
        cmd = [
            sys.executable,
            "run.py",
            "--jd",
            "data/jd.txt",
            "--input",
            "data/sample_candidates.json",
            "--output",
            "outputs/submission.csv",
        ]

        # Process run
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            csv_path = "outputs/submission.csv"
            if os.path.exists(csv_path):
                df = pd.read_csv(csv_path)

                st.success(
                    "Candidate Ranking Completed and Validated Successfully"
                )

                m_col1, m_col2, m_col3 = st.columns(3)
                with m_col1:
                    st.metric(label="Total Candidates Ranked", value=len(df))
                with m_col2:
                    st.metric(
                        label="Maximum Match Score",
                        value=f"{df['score'].max():.3f}",
                    )
                with m_col3:
                    st.metric(
                        label="Minimum Match Score",
                        value=f"{df['score'].min():.3f}",
                    )

                st.subheader("Ranked Candidates Leaderboard")

                st.dataframe(
                    df,
                    use_container_width=True,
                    column_config={
                        "candidate_id": st.column_config.TextColumn(
                            "Candidate ID", width="medium"
                        ),
                        "rank": st.column_config.NumberColumn(
                            "Rank", width="small"
                        ),
                        "score": st.column_config.NumberColumn(
                            "Score", width="small", format="%.3f"
                        ),
                        "reasoning": st.column_config.TextColumn(
                            "Reasoning Explanation", width="large"
                        ),
                    },
                )

                st.subheader("Execution Logs")
                st.code(result.stdout)
            else:
                st.error(
                    "Output file 'outputs/submission.csv' was not found after execution."
                )
        else:
            st.error("Pipeline Execution Error")
            st.code(result.stderr)
else:
    st.markdown("<br>", unsafe_allow_html=True)
    st.info(
        "Click the 'Run Ranking Pipeline' button above to execute and view the leaderboard."
    )
