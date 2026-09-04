import os
import re
from pathlib import Path
from textwrap import dedent

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# Load .env from the same folder as app.py
try:
    from dotenv import load_dotenv
    ENV_FILE = Path(__file__).resolve().parent / ".env"
    load_dotenv(ENV_FILE, override=True)
except ImportError:
    ENV_FILE = Path(__file__).resolve().parent / ".env"

from resume_parser import extract_text_from_pdf
from skill_extractor import (
    extract_skills,
    get_skill_evidence,
    calculate_skill_score,
)

# ============================================================
# AI AGENTS
# ============================================================

try:
    from ai_agents import (
        AICareerManager,
        InterviewAgent,
        ResumeImprovementAgent,
    )
except ImportError:
    AICareerManager = None
    InterviewAgent = None
    ResumeImprovementAgent = None


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Job Readiness Analyzer",
    page_icon="J",
    layout="wide",
)


# ============================================================
# LOAD CSS
# ============================================================

css_path = Path(__file__).with_name("style.css")


def render_html(content):
    """Render the existing dashboard HTML without changing its design."""
    if not isinstance(content, str):
        content = str(content)
    content = dedent(content).strip()

    # Use Streamlit's native HTML renderer for actual HTML.
    # Keep Markdown headings as Markdown so the existing AI labels
    # such as "### Resume Agent" continue to render correctly.
    if content.startswith("<") or "<div" in content or "<section" in content:
        if hasattr(st, "html"):
            st.html(content)
        else:
            st.markdown(content, unsafe_allow_html=True)
    else:
        st.markdown(content)

if css_path.exists():
    css_text = css_path.read_text(encoding="utf-8")
    if hasattr(st, "html"):
        st.html(f"<style>{css_text}</style>")
    else:
        st.markdown(f"<style>{css_text}</style>", unsafe_allow_html=True)


# ============================================================
# ROLE DATABASE
# ============================================================

ROLES = {
    "Data Analyst": {
        "skills": {
            "Python": 80,
            "SQL": 85,
            "Excel": 80,
            "Power BI": 80,
            "Statistics": 80,
            "Data Visualization": 75,
            "Communication": 80,
        },
        "terms": {
            "Python": [
                "python",
                "pandas",
                "numpy",
                "scikit-learn",
                "sklearn",
            ],
            "SQL": [
                "sql",
                "mysql",
                "postgresql",
                "postgres",
                "sqlite",
                "database",
            ],
            "Excel": [
                "excel",
                "pivot table",
                "pivottable",
                "vlookup",
                "xlookup",
                "spreadsheet",
            ],
            "Power BI": [
                "power bi",
                "powerbi",
                "power query",
                "dax",
            ],
            "Statistics": [
                "statistics",
                "statistical",
                "probability",
                "hypothesis testing",
                "regression",
                "correlation",
            ],
            "Data Visualization": [
                "data visualization",
                "data visualisation",
                "visualization",
                "visualisation",
                "matplotlib",
                "seaborn",
                "plotly",
                "tableau",
                "dashboard",
            ],
            "Communication": [
                "communication",
                "presentation",
                "presentations",
                "presented",
                "stakeholder",
                "reporting",
            ],
        },
    },

    "Software Developer": {
        "skills": {
            "Python": 80,
            "SQL": 70,
            "Git": 75,
            "JavaScript": 75,
            "Problem Solving": 80,
            "APIs": 70,
            "Communication": 70,
        },
        "terms": {
            "Python": [
                "python",
                "django",
                "flask",
                "fastapi",
            ],
            "SQL": [
                "sql",
                "mysql",
                "postgresql",
                "database",
            ],
            "Git": [
                "git",
                "github",
                "gitlab",
                "version control",
            ],
            "JavaScript": [
                "javascript",
                "node.js",
                "nodejs",
                "react",
                "typescript",
            ],
            "Problem Solving": [
                "problem solving",
                "problem-solving",
                "algorithms",
                "data structures",
                "debugging",
            ],
            "APIs": [
                "api",
                "apis",
                "rest api",
                "restful",
                "json",
            ],
            "Communication": [
                "communication",
                "presentation",
                "teamwork",
                "collaboration",
            ],
        },
    },

    "Machine Learning Engineer": {
        "skills": {
            "Python": 85,
            "Machine Learning": 85,
            "SQL": 70,
            "Statistics": 80,
            "Deep Learning": 75,
            "Git": 70,
            "Problem Solving": 80,
        },
        "terms": {
            "Python": [
                "python",
                "pandas",
                "numpy",
            ],
            "Machine Learning": [
                "machine learning",
                "scikit-learn",
                "sklearn",
                "classification",
                "clustering",
                "regression",
            ],
            "SQL": [
                "sql",
                "mysql",
                "postgresql",
                "database",
            ],
            "Statistics": [
                "statistics",
                "statistical",
                "probability",
                "hypothesis testing",
                "correlation",
                "regression",
            ],
            "Deep Learning": [
                "deep learning",
                "tensorflow",
                "keras",
                "pytorch",
                "neural network",
                "cnn",
                "rnn",
            ],
            "Git": [
                "git",
                "github",
                "gitlab",
                "version control",
            ],
            "Problem Solving": [
                "problem solving",
                "problem-solving",
                "algorithms",
                "data structures",
                "debugging",
            ],
        },
    },

    "Business Analyst": {
        "skills": {
            "Excel": 85,
            "SQL": 70,
            "Power BI": 75,
            "Communication": 90,
            "Problem Solving": 80,
            "Statistics": 65,
            "Data Visualization": 75,
        },
        "terms": {
            "Excel": [
                "excel",
                "pivot table",
                "pivottable",
                "vlookup",
                "xlookup",
            ],
            "SQL": [
                "sql",
                "mysql",
                "postgresql",
                "database",
            ],
            "Power BI": [
                "power bi",
                "powerbi",
                "power query",
                "dax",
            ],
            "Communication": [
                "communication",
                "presentation",
                "presentations",
                "stakeholder",
                "client",
                "reporting",
                "documentation",
            ],
            "Problem Solving": [
                "problem solving",
                "problem-solving",
                "requirements",
                "analysis",
                "business analysis",
            ],
            "Statistics": [
                "statistics",
                "probability",
                "regression",
                "correlation",
            ],
            "Data Visualization": [
                "data visualization",
                "data visualisation",
                "visualization",
                "dashboard",
                "tableau",
                "plotly",
            ],
        },
    },

    "Data Scientist": {
        "skills": {
            "Python": 85,
            "SQL": 75,
            "Statistics": 90,
            "Machine Learning": 90,
            "Data Visualization": 80,
            "Problem Solving": 85,
            "Communication": 75,
        },
        "terms": {
            "Python": [
                "python",
                "pandas",
                "numpy",
            ],
            "SQL": [
                "sql",
                "mysql",
                "postgresql",
                "database",
            ],
            "Statistics": [
                "statistics",
                "statistical",
                "probability",
                "hypothesis testing",
                "regression",
                "correlation",
            ],
            "Machine Learning": [
                "machine learning",
                "scikit-learn",
                "sklearn",
                "classification",
                "clustering",
                "regression",
            ],
            "Data Visualization": [
                "data visualization",
                "data visualisation",
                "visualization",
                "matplotlib",
                "seaborn",
                "plotly",
                "tableau",
            ],
            "Problem Solving": [
                "problem solving",
                "problem-solving",
                "algorithms",
                "data structures",
                "debugging",
            ],
            "Communication": [
                "communication",
                "presentation",
                "presentations",
                "stakeholder",
                "reporting",
            ],
        },
    },
}


# ============================================================
# ACTION PLAN TIPS
# ============================================================

TIPS = {
    "Python":
        "Build a practical Python project using pandas, functions, file handling and data processing.",

    "SQL":
        "Practice SELECT, JOIN, GROUP BY, CTEs and window functions on real datasets.",

    "Excel":
        "Practice PivotTables, XLOOKUP, formulas, conditional formatting and dashboards.",

    "Power BI":
        "Build a dashboard using Power Query, data modelling, DAX measures and filters.",

    "Statistics":
        "Revise probability, hypothesis testing, correlation, regression and descriptive statistics.",

    "Data Visualization":
        "Create dashboards with clear KPIs, chart selection and data storytelling.",

    "Communication":
        "Practice explaining projects using problem, approach and measurable result.",

    "Git":
        "Use commits, branches, pull requests and GitHub repositories in your projects.",

    "JavaScript":
        "Build small projects and practice DOM, ES6, APIs and asynchronous JavaScript.",

    "Problem Solving":
        "Solve coding problems regularly and document your approach.",

    "APIs":
        "Build a REST API client and practice HTTP methods, JSON and error handling.",

    "Machine Learning":
        "Build classification and regression projects with preprocessing and evaluation.",

    "Deep Learning":
        "Build a small neural-network project and explain its training pipeline.",
}


# ============================================================
# SUITABLE JOB OPTIONS
# ============================================================

JOB_OPTIONS = {
    "Data Analyst": [
        "Junior Data Analyst",
        "Business Intelligence Analyst",
        "Reporting Analyst",
        "MIS Analyst",
        "Junior BI Developer",
    ],

    "Software Developer": [
        "Junior Software Developer",
        "Python Developer",
        "Backend Developer",
        "Full Stack Developer",
        "Software Engineer Trainee",
    ],

    "Machine Learning Engineer": [
        "Junior Machine Learning Engineer",
        "ML Intern",
        "AI Engineer Intern",
        "Data Science Intern",
        "Junior Data Scientist",
    ],

    "Business Analyst": [
        "Junior Business Analyst",
        "Business Intelligence Analyst",
        "Process Analyst",
        "Reporting Analyst",
        "Operations Analyst",
    ],

    "Data Scientist": [
        "Junior Data Scientist",
        "Data Science Intern",
        "Junior ML Engineer",
        "Analytics Associate",
        "Data Analyst",
    ],
}


# ============================================================
# SESSION STATE
# ============================================================

DEFAULT_STATE = {
    "df": None,
    "text": "",
    "role": "",
    "name": "",
    "detected_skills": [],
    "skill_evidence": {},
    "ai_results": None,
    "ai_resume_improvement": None,
    "ai_interview_questions": None,
    "interview_feedback": None,
}

for key, value in DEFAULT_STATE.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def score(text, terms):
    """
    Calculate evidence-based score for a group of skill terms.
    """
    if not text:
        return 0

    text_lower = text.lower()
    hits = 0

    for term in terms:
        pattern = (
            r"(?<![a-z0-9])"
            + re.escape(term.lower())
            + r"(?![a-z0-9])"
        )

        if re.search(pattern, text_lower):
            hits += 1

    if hits == 0:
        return 0

    return min(100, 45 + 18 * hits)


def analyze(text, role):
    """
    Compare resume skill evidence with role requirements.
    """
    profile = ROLES[role]

    rows = []

    for skill, target in profile["skills"].items():

        current = score(
            text,
            profile["terms"][skill],
        )

        gap = current - target

        if current >= target:
            status = "Strength"
        elif current < target - 25:
            status = "Critical"
        else:
            status = "Below target"

        rows.append(
            {
                "Skill": skill,
                "Current": current,
                "Target": target,
                "Gap": gap,
                "Status": status,
            }
        )

    return pd.DataFrame(rows)


def readiness(df):
    """
    Overall requirement coverage.
    """
    if df is None or df.empty:
        return 0.0

    coverage = (
        df["Current"] / df["Target"]
    ).clip(0, 1)

    return round(
        float(coverage.mean() * 100),
        1,
    )


def get_job_match(df):
    """
    Resume-to-role match score.
    """
    return readiness(df)


def get_gaps(df):
    """
    Return skill names below target.
    """
    if df is None or df.empty:
        return []

    return [
        row["Skill"]
        for _, row in df.iterrows()
        if row["Current"] < row["Target"]
    ]


def build_skill_data(df):
    """
    Convert dataframe into AI-friendly dictionaries.
    """
    if df is None or df.empty:
        return []

    records = []

    for _, row in df.iterrows():
        records.append(
            {
                "skill": str(row["Skill"]),
                "current": int(row["Current"]),
                "target": int(row["Target"]),
                "gap": int(row["Gap"]),
                "status": str(row["Status"]),
            }
        )

    return records


def radar(df):
    """
    Create radar chart.
    """
    if df is None or df.empty:
        return go.Figure()

    labels = (
        df["Skill"].tolist()
        + [df["Skill"].iloc[0]]
    )

    current = (
        df["Current"].tolist()
        + [df["Current"].iloc[0]]
    )

    target = (
        df["Target"].tolist()
        + [df["Target"].iloc[0]]
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatterpolar(
            r=target,
            theta=labels,
            name="Target",
            mode="lines+markers",
            line=dict(
                color="#5B6CFF",
                width=3,
                dash="dot",
            ),
            marker=dict(size=7),
            fill="toself",
            fillcolor="rgba(91,108,255,.05)",
        )
    )

    fig.add_trace(
        go.Scatterpolar(
            r=current,
            theta=labels,
            name="Current",
            mode="lines+markers",
            line=dict(
                color="#6FB56A",
                width=3,
            ),
            marker=dict(size=7),
            fill="toself",
            fillcolor="rgba(111,181,106,.22)",
        )
    )

    fig.update_layout(
        height=500,
        margin=dict(
            l=45,
            r=45,
            t=30,
            b=45,
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickvals=[
                    20,
                    40,
                    60,
                    80,
                    100,
                ],
                gridcolor="#E5E7EB",
                tickfont=dict(
                    color="#667085"
                ),
            ),
            angularaxis=dict(
                gridcolor="#E5E7EB",
                tickfont=dict(
                    color="#334155"
                ),
            ),
        ),
        legend=dict(
            orientation="h",
            y=-0.12,
            x=0.5,
            xanchor="center",
        ),
        font=dict(
            family="Inter"
        ),
    )

    return fig


def reset_ai_results():
    """
    Clear AI results after a new resume analysis.
    """
    st.session_state.ai_results = None
    st.session_state.ai_resume_improvement = None
    st.session_state.ai_interview_questions = None
    st.session_state.interview_feedback = None


# ============================================================
# INITIALIZE AI ENGINE
# ============================================================

ai_engine = None
interview_agent = None
resume_improvement_agent = None

if AICareerManager is not None:

    try:
        ai_engine = AICareerManager()

        if InterviewAgent is not None:
            interview_agent = InterviewAgent(
                ai_engine.ai
            )

        if ResumeImprovementAgent is not None:
            resume_improvement_agent = (
                ResumeImprovementAgent(
                    ai_engine.ai
                )
            )

    except Exception:
        ai_engine = None


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    render_html(
        '<div class="side-title">Analyzer Settings</div>',
    )

    # AI connection status
    if os.getenv("OPENROUTER_API_KEY", "").strip():
        st.success("OpenRouter API key detected")
    else:
        st.error(f"OpenRouter API key not found\n\nExpected: {ENV_FILE}")

    role = st.selectbox(
        "Target Job Role",
        list(ROLES),
        index=(
            list(ROLES).index(st.session_state.role)
            if st.session_state.role in ROLES
            else 0
        ),
    )

    upload = st.file_uploader(
        "Upload Resume",
        type=["pdf"],
        key="resume_uploader",
    )

    render_html(
        """
        <div class="side-note">
            Upload a text-based PDF resume.
            The score is an estimate based on resume evidence.
        </div>
        """,
    )

    analyze_clicked = st.button(
        "Analyze Resume",
        type="primary",
        use_container_width=True,
    )

    if upload:

        render_html(
            f"""
            <div class="file-box">

                <b>{upload.name}</b>

                <br>

                <span>
                    {upload.size / 1024:.1f} KB · PDF ready
                </span>

            </div>
            """,
    )


# ============================================================
# ANALYZE RESUME
# ============================================================

if analyze_clicked:

    if upload is None:

        st.error(
            "Please upload a PDF resume first."
        )

    else:

        try:

            with st.spinner(
                "Reading and analyzing your resume..."
            ):

                text = extract_text_from_pdf(
                    upload
                )

            if not text:

                st.error(
                    "No readable text was found. "
                    "Please upload a text-based PDF."
                )

            elif text.startswith("PDF_ERROR:"):

                st.error(text)

            else:

                detected_skills = extract_skills(
                    text
                )

                skill_evidence = get_skill_evidence(
                    text
                )

                result_df = analyze(
                    text,
                    role,
                )

                st.session_state.df = result_df
                st.session_state.text = text
                st.session_state.role = role
                st.session_state.name = upload.name
                st.session_state.detected_skills = (
                    detected_skills
                )
                st.session_state.skill_evidence = (
                    skill_evidence
                )

                reset_ai_results()

                st.success(
                    "Resume analyzed successfully."
                )

        except Exception as exc:

            st.error(
                f"PDF analysis failed: {exc}"
            )


# ============================================================
# HEADER
# ============================================================

render_html(
    """
    <div class="topbar">

        <div>

            <div class="brand-title">
                Job Readiness Analyzer
            </div>

            <div class="brand-subtitle">
                Resume intelligence and career skill analysis
            </div>

        </div>

        <div class="header-pill">
            CAREER ANALYTICS
        </div>

    </div>
    """,
    )


# ============================================================
# LANDING PAGE
# ============================================================

if st.session_state.df is None:

    render_html(
        """
        <section class="hero">

            <div class="hero-label">
                CAREER READINESS PLATFORM
            </div>

            <h1>
                Understand where you stand<br>
                for your target job.
            </h1>

            <p>
                Upload your resume and select a target role.
                The analyzer extracts relevant skills,
                measures job readiness and identifies the
                areas you should improve.
            </p>

        </section>
        """,
    )

    # --------------------------------------------------------
    # WHAT THIS PLATFORM DOES
    # --------------------------------------------------------

    render_html(
        '<div class="section-title">What this platform does</div>',
    )

    cards = [
        (
            "01",
            "Resume Analysis",
            "Extract technical and professional skills directly from your resume.",
        ),
        (
            "02",
            "Skill Gap Analysis",
            "Compare your current skills with the requirements of your target role.",
        ),
        (
            "03",
            "Career Action Plan",
            "Identify the skills you need to improve for your target job.",
        ),
    ]

    cols = st.columns(3)

    for col, (num, title, desc) in zip(
        cols,
        cards,
    ):

        with col:

            render_html(
                f"""
                <div class="feature-card">

                    <div class="card-number">
                        {num}
                    </div>

                    <div class="card-title">
                        {title}
                    </div>

                    <div class="card-text">
                        {desc}
                    </div>

                </div>
                """,
    )

    # --------------------------------------------------------
    # HOW IT WORKS
    # --------------------------------------------------------

    render_html(
        '<div class="section-title">How it works</div>',
    )

    steps = [
        (
            "STEP 01",
            "Select your role",
            "Choose the job you want to prepare for.",
        ),
        (
            "STEP 02",
            "Upload resume",
            "Upload your PDF resume for automatic analysis.",
        ),
        (
            "STEP 03",
            "Get your analysis",
            "View your readiness score, skill gaps and recommendations.",
        ),
    ]

    cols = st.columns(3)

    for col, (num, title, desc) in zip(
        cols,
        steps,
    ):

        with col:

            render_html(
                f"""
                <div class="feature-card">

                    <div class="card-number">
                        {num}
                    </div>

                    <div class="card-title">
                        {title}
                    </div>

                    <div class="card-text">
                        {desc}
                    </div>

                </div>
                """,
    )

    st.stop()


# ============================================================
# DASHBOARD DATA
# ============================================================

df = st.session_state.df

active = st.session_state.role

ready = readiness(df)

role_match = get_job_match(df)

strengths = int(
    (
        df["Current"] >= df["Target"]
    ).sum()
)

critical = int(
    (
        df["Current"] < df["Target"] - 25
    ).sum()
)

total_gap = int(
    (
        df["Current"] - df["Target"]
    ).sum()
)

avg_gap = float(
    (
        df["Current"] - df["Target"]
    ).mean()
)

skill_gaps = get_gaps(df)


# ============================================================
# ANALYSIS HEADER
# ============================================================

render_html(
    f"""
    <div class="analysis-head">

        <div>

            <div class="hero-label">
                RESUME ANALYSIS
            </div>

            <h2>
                {active}
            </h2>

            <p>
                {st.session_state.name}
                · Analysis complete
            </p>

        </div>

        <div class="ready-badge">
            ANALYSIS READY
        </div>

    </div>
    """,
    )


# ============================================================
# MAIN METRICS
# ============================================================

cols = st.columns(4)

metrics = [
    (
        "READINESS",
        f"{ready:.0f}%",
        "Overall requirement coverage",
    ),
    (
        "ROLE MATCH",
        f"{role_match:.0f}%",
        "Resume-to-role match",
    ),
    (
        "STRENGTHS",
        str(strengths),
        "Meeting target",
    ),
    (
        "CRITICAL GAPS",
        str(critical),
        "Need attention",
    ),
]

for col, (label, value, desc) in zip(
    cols,
    metrics,
):

    with col:

        render_html(
            f"""
            <div class="metric-card">

                <div class="metric-label">
                    {label}
                </div>

                <div class="metric-value">
                    {value}
                </div>

                <div class="metric-desc">
                    {desc}
                </div>

            </div>
            """,
    )


# ============================================================
# DETECTED RESUME SKILLS
# ============================================================

render_html(
    '<div class="section-title">Detected Resume Skills</div>',
    )

detected_skills = st.session_state.detected_skills

if detected_skills:

    cols = st.columns(4)

    for index, skill in enumerate(
        detected_skills
    ):

        skill_score = calculate_skill_score(
            st.session_state.text,
            skill,
        )

        with cols[index % 4]:

            st.metric(
                label=skill,
                value=f"{skill_score}%",
            )

else:

    st.warning(
        "No matching skills were detected in the resume."
    )


# ============================================================
# RESUME TO JOB MATCH
# ============================================================

render_html(
    '<div class="section-title">Resume to Job Match</div>',
    )

cols = st.columns(3)

keyword_score = round(
    (
        df["Current"].gt(0).sum()
        / len(df)
    ) * 100
)

skill_score_avg = round(
    df["Current"].mean()
)

match_values = [
    keyword_score,
    skill_score_avg,
    round(ready),
]

match_labels = [
    "Keywords",
    "Skills",
    "Requirement fit",
]

for col, value, label in zip(
    cols,
    match_values,
    match_labels,
):

    with col:

        render_html(
            f"""
            <div class="circle-card">

                <div class="circle-value">
                    {value}%
                </div>

                <div class="circle-label">
                    {label}
                </div>

            </div>
            """,
    )


# ============================================================
# SUITABLE JOB OPPORTUNITIES
# ============================================================

render_html(
    '<div class="section-title">Suitable Job Opportunities</div>',
    )

st.caption(
    "Based on your selected role and current resume skill profile."
)

suitable_jobs = JOB_OPTIONS.get(
    active,
    [],
)

job_cols = st.columns(3)

for index, job in enumerate(
    suitable_jobs
):

    with job_cols[index % 3]:

        render_html(
            f"""
            <div class="action-card">

                <div class="action-title">
                    {job}
                </div>

                <div class="action-text">
                    Entry-level opportunity aligned
                    with your {active} career path.
                </div>

            </div>
            """,
    )


# ============================================================
# SKILLS GAP ANALYSIS
# ============================================================

render_html(
    '<div class="section-title">Skills Gap Analysis</div>',
    )

st.caption(
    "Compare your current skill levels with target job requirements."
)

cols = st.columns(4)

summary = [
    (
        "TOTAL GAP",
        f"{total_gap:+d}",
        "Points below target",
    ),
    (
        "AVERAGE GAP",
        f"{avg_gap:+.1f}",
        "Per skill area",
    ),
    (
        "CRITICAL GAPS",
        str(critical),
        "Need immediate attention",
    ),
    (
        "STRENGTHS",
        str(strengths),
        "Meeting expectations",
    ),
]

for col, (label, value, desc) in zip(
    cols,
    summary,
):

    with col:

        render_html(
            f"""
            <div class="summary-card">

                <div class="summary-value">
                    {value}
                </div>

                <div class="summary-label">
                    {label}
                </div>

                <div class="summary-desc">
                    {desc}
                </div>

            </div>
            """,
    )


# ============================================================
# RADAR + SKILL COMPARISON
# ============================================================

chart_col, detail_col = st.columns(
    [1.25, 1]
)

with chart_col:

    render_html(
        '<div class="panel-title">Skills Radar Chart</div>',
    )

    st.plotly_chart(
        radar(df),
        use_container_width=True,
        config={
            "displayModeBar": False
        },
    )


with detail_col:

    render_html(
        '<div class="panel-title">Skill comparison</div>',
    )

    for _, row in df.iterrows():

        cls = (
            "good"
            if row["Status"] == "Strength"
            else (
                "critical"
                if row["Status"] == "Critical"
                else "below"
            )
        )

        render_html(
            f"""
            <div class="skill-row">

                <div class="skill-top">

                    <b>
                        {row["Skill"]}
                    </b>

                    <span class="status {cls}">
                        {row["Status"]}
                    </span>

                </div>

                <div class="skill-values">

                    <span>
                        Current: {int(row["Current"])}%
                    </span>

                    <span>
                        Target: {int(row["Target"])}%
                    </span>

                </div>

                <div class="track">

                    <div
                        class="current"
                        style="width:{int(row["Current"])}%"
                    ></div>

                </div>

                <div class="gap">
                    Gap: {int(row["Gap"]):+d}
                </div>

            </div>
            """,
    )


# ============================================================
# SKILL DETAILS
# ============================================================

render_html(
    '<div class="section-title">Skill Details</div>',
    )

st.caption(
    "Detailed comparison of your current skills with target levels."
)

cols = st.columns(3)

for index, (_, row) in enumerate(
    df.iterrows()
):

    cls = (
        "good"
        if row["Status"] == "Strength"
        else (
            "critical"
            if row["Status"] == "Critical"
            else "below"
        )
    )

    with cols[index % 3]:

        render_html(
            f"""
            <div class="detail-card">

                <div class="skill-top">

                    <b>
                        {row["Skill"]}
                    </b>

                    <span class="status {cls}">
                        {row["Status"]}
                    </span>

                </div>

                <div class="skill-values">

                    <span>
                        Current: {int(row["Current"])}%
                    </span>

                    <span>
                        Target: {int(row["Target"])}%
                    </span>

                </div>

                <div class="track">

                    <div
                        class="current"
                        style="width:{int(row["Current"])}%"
                    ></div>

                </div>

                <div class="gap">
                    Gap: {int(row["Gap"]):+d}
                </div>

            </div>
            """,
    )


# ============================================================
# RECOMMENDED ACTION PLAN
# ============================================================

render_html(
    '<div class="section-title">Recommended Action Plan</div>',
    )

st.caption(
    "Focus on the largest gaps first."
)

gap_rows = (
    df.sort_values(
        "Gap",
        ascending=True,
    )
    .head(5)
)

for _, row in gap_rows.iterrows():

    need = int(
        row["Target"] - row["Current"]
    )

    if need > 0:

        tip = TIPS.get(
            row["Skill"],
            (
                f"Build a practical "
                f"{row['Skill']} project and "
                "add measurable evidence to your resume."
            ),
        )

        render_html(
            f"""
            <div class="action-card">

                <div class="action-title">
                    {row["Skill"]}
                </div>

                <div class="action-text">
                    Gap of <b>{need} points</b>.
                    {tip}
                </div>

            </div>
            """,
    )


# ============================================================
# AI CAREER AGENTS
# ============================================================

render_html(
    '<div class="section-title">AI Career Agents</div>',
    )

st.caption(
    "AI agents analyze your resume from multiple career perspectives."
)

if ai_engine is None:

    st.warning(
        "AI is not connected. "
        "Check that ai_agents.py exists and is error-free."
    )

elif not ai_engine.available:

    st.warning(
        "AI is not connected. "
        "Add OPENROUTER_API_KEY to your .env file."
    )

else:

    if st.session_state.ai_results is None:

        if st.button(
            "Run AI Career Agents",
            type="primary",
            use_container_width=True,
        ):

            with st.spinner(
                "AI agents are analyzing your resume..."
            ):

                try:

                    st.session_state.ai_results = (
                        ai_engine.run(
                            resume_text=st.session_state.text,
                            skills=st.session_state.detected_skills,
                            role=active,
                            match_score=role_match,
                            readiness_score=ready,
                            gaps=skill_gaps,
                            skill_data=build_skill_data(df),
                        )
                    )

                    st.success(
                        "AI Career Agents completed the analysis."
                    )

                except Exception as exc:

                    st.error(
                        f"AI analysis failed: {exc}"
                    )

    else:

        tabs = st.tabs(
            [
                "Resume Agent",
                "Skill Gap Agent",
                "Job Match Agent",
                "Career Coach",
            ]
        )

        with tabs[0]:

            render_html(
                "### Resume Agent"
            )

            st.write(
                st.session_state.ai_results.get(
                    "resume",
                    "No result available.",
                )
            )

        with tabs[1]:

            render_html(
                "### Skill Gap Agent"
            )

            st.write(
                st.session_state.ai_results.get(
                    "skill_gap",
                    "No result available.",
                )
            )

        with tabs[2]:

            render_html(
                "### Job Match Agent"
            )

            st.write(
                st.session_state.ai_results.get(
                    "job_match",
                    "No result available.",
                )
            )

        with tabs[3]:

            render_html(
                "### Career Coach"
            )

            st.write(
                st.session_state.ai_results.get(
                    "career_coach",
                    "No result available.",
                )
            )

        if st.button(
            "Run AI Career Agents Again",
            use_container_width=True,
        ):

            reset_ai_results()

            st.rerun()


# ============================================================
# AI CAREER MANAGER
# ============================================================

render_html(
    '<div class="section-title">AI Career Manager</div>',
    )

st.caption(
    "Get a combined AI view of your career readiness."
)

if ai_engine is None:

    st.info(
        "AI Career Manager is unavailable."
    )

elif not ai_engine.available:

    st.info(
        "Connect OpenRouter to use AI Career Manager."
    )

else:

    manager_cols = st.columns(4)

    manager_items = [
        (
            "Resume",
            "Resume Agent",
            "Resume strengths and improvement areas.",
        ),
        (
            "Skills",
            "Skill Gap Agent",
            "Priority skill gaps to work on.",
        ),
        (
            "Jobs",
            "Job Match Agent",
            "Suitable adjacent entry-level opportunities.",
        ),
        (
            "Career",
            "Career Coach",
            "Practical next-step career roadmap.",
        ),
    ]

    for col, (num, title, desc) in zip(
        manager_cols,
        manager_items,
    ):

        with col:

            render_html(
                f"""
                <div class="feature-card">

                    <div class="card-number">
                        {num}
                    </div>

                    <div class="card-title">
                        {title}
                    </div>

                    <div class="card-text">
                        {desc}
                    </div>

                </div>
                """,
    )


# ============================================================
# AI RESUME IMPROVEMENT
# ============================================================

render_html(
    '<div class="section-title">AI Resume Improvement</div>',
    )

st.caption(
    "Get AI-powered suggestions for improving your resume for the selected role."
)

if resume_improvement_agent is None:

    st.info(
        "Resume Improvement Agent is unavailable."
    )

elif ai_engine is None or not ai_engine.available:

    st.warning(
        "Connect OpenRouter to use AI Resume Improvement."
    )

else:

    if st.session_state.ai_resume_improvement is None:

        if st.button(
            "Improve My Resume with AI",
            use_container_width=True,
        ):

            with st.spinner(
                "AI is reviewing your resume..."
            ):

                result = (
                    resume_improvement_agent.run(
                        role=active,
                        resume_text=st.session_state.text,
                        skills=st.session_state.detected_skills,
                    )
                )

                st.session_state.ai_resume_improvement = result

            st.rerun()

    else:

        with st.container(
            border=True
        ):

            render_html(
                "### AI Resume Recommendations"
            )

            st.write(
                st.session_state.ai_resume_improvement
            )

        if st.button(
            "Generate New Resume Suggestions",
            use_container_width=True,
        ):

            st.session_state.ai_resume_improvement = None

            st.rerun()


# ============================================================
# AI INTERVIEW PREPARATION
# ============================================================

render_html(
    '<div class="section-title">AI Interview Preparation</div>',
    )

st.caption(
    "Generate role-specific interview questions and practice your answers."
)

if interview_agent is None:

    st.info(
        "Interview Agent is unavailable."
    )

elif ai_engine is None or not ai_engine.available:

    st.warning(
        "Connect OpenRouter to use AI Interview Preparation."
    )

else:

    if st.session_state.ai_interview_questions is None:

        if st.button(
            "Generate Interview Questions",
            use_container_width=True,
        ):

            with st.spinner(
                "Preparing interview questions..."
            ):

                result = (
                    interview_agent.generate_questions(
                        role=active,
                        resume_text=st.session_state.text,
                    )
                )

                st.session_state.ai_interview_questions = result

            st.rerun()

    else:

        with st.container(
            border=True
        ):

            render_html(
                "### Interview Questions & Model Answers"
            )

            st.write(
                st.session_state.ai_interview_questions
            )

        if st.button(
            "Generate New Questions",
            use_container_width=True,
        ):

            st.session_state.ai_interview_questions = None

            st.rerun()

    # --------------------------------------------------------
    # ANSWER PRACTICE
    # --------------------------------------------------------

    render_html(
        "### Practice an Interview Question"
    )

    practice_question = st.text_input(
        "Interview Question",
        placeholder="Example: Explain one project from your resume.",
    )

    practice_answer = st.text_area(
        "Your Answer",
        height=180,
        placeholder="Write your interview answer here...",
    )

    if st.button(
        "Evaluate My Answer",
        use_container_width=True,
    ):

        if not practice_question.strip():

            st.error(
                "Please enter an interview question."
            )

        elif not practice_answer.strip():

            st.error(
                "Please write your answer first."
            )

        else:

            with st.spinner(
                "AI is evaluating your answer..."
            ):

                feedback = (
                    interview_agent.evaluate_answer(
                        role=active,
                        question=practice_question,
                        answer=practice_answer,
                    )
                )

                st.session_state.interview_feedback = (
                    feedback
                )

    if st.session_state.interview_feedback:

        with st.container(
            border=True
        ):

            render_html(
                "### AI Interview Feedback"
            )

            st.write(
                st.session_state.interview_feedback
            )


# ============================================================
# RESUME ANALYSIS
# ============================================================

render_html(
    '<div class="section-title">Resume Analysis</div>',
    )

with st.expander(
    "View extracted resume text"
):

    st.text_area(
        "Extracted text",
        st.session_state.text,
        height=280,
        label_visibility="collapsed",
    )


# ============================================================
# CSV DOWNLOAD
# ============================================================

csv_data = df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    "Download Skill Analysis CSV",
    csv_data,
    "skill_analysis.csv",
    "text/csv",
)


# ============================================================
# FOOTER
# ============================================================

render_html(
    """
    <div class="footer">
        Job Readiness Analyzer · Resume Intelligence · Skill Gap Analysis
    </div>
    """,
    )