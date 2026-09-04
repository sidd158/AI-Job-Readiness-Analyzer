import streamlit as st

st.set_page_config(
    page_title="Job Readiness Analyzer",
    layout="wide"
)

st.markdown("""
<style>

.stApp {
    background: #f5f7fb;
}

.block-container {
    max-width: 1400px;
    padding: 40px;
}

.header {
    background: white;
    padding: 25px 30px;
    border-radius: 20px;
    border: 1px solid #e1e5ed;
    margin-bottom: 25px;
}

.title {
    font-size: 32px;
    font-weight: 800;
    color: #182238;
}

.subtitle {
    color: #7c8799;
    margin-top: 5px;
}

.badge {
    display: inline-block;
    margin-top: 15px;
    padding: 8px 15px;
    border-radius: 20px;
    background: #eef0ff;
    color: #5968c2;
    font-size: 11px;
    font-weight: bold;
    letter-spacing: 1px;
}

.hero {
    background: white;
    padding: 45px;
    border-radius: 25px;
    border: 1px solid #e1e5ed;
    margin-bottom: 30px;
}

.hero-label {
    color: #5968c2;
    font-size: 11px;
    font-weight: bold;
    letter-spacing: 2px;
}

.hero-title {
    color: #182238;
    font-size: 44px;
    font-weight: 800;
    margin-top: 15px;
}

.hero-text {
    color: #7c8799;
    font-size: 16px;
    line-height: 1.7;
    max-width: 750px;
}

.section {
    color: #182238;
    font-size: 24px;
    font-weight: 800;
    margin: 30px 0 18px 0;
}

.card {
    background: white;
    padding: 28px;
    border-radius: 18px;
    border: 1px solid #e1e5ed;
    min-height: 170px;
}

.number {
    color: #5968c2;
    font-size: 12px;
    font-weight: bold;
}

.card-title {
    color: #202b42;
    font-size: 19px;
    font-weight: 800;
    margin-top: 12px;
}

.card-text {
    color: #7c8799;
    font-size: 14px;
    line-height: 1.6;
    margin-top: 8px;
}

.footer {
    text-align: center;
    color: #9099a8;
    margin-top: 50px;
    padding: 25px;
}

</style>
""", unsafe_allow_html=True)


# HEADER

st.markdown("""
<div class="header">

    <div class="title">
        Job Readiness Analyzer
    </div>

    <div class="subtitle">
        Resume intelligence and career skill analysis
    </div>

    <div class="badge">
        CAREER ANALYTICS
    </div>

</div>
""", unsafe_allow_html=True)


# HERO

st.markdown("""
<div class="hero">

    <div class="hero-label">
        CAREER READINESS PLATFORM
    </div>

    <div class="hero-title">
        Understand where you stand
        for your target job.
    </div>

    <div class="hero-text">
        Upload your resume and select a target role.
        The analyzer extracts relevant skills,
        measures job readiness and identifies
        the areas you should improve.
    </div>

</div>
""", unsafe_allow_html=True)


# FEATURES

st.markdown(
    '<div class="section">What this platform does</div>',
    unsafe_allow_html=True
)

c1, c2, c3 = st.columns(3)

with c1:

    st.markdown("""
    <div class="card">

        <div class="number">01</div>

        <div class="card-title">
            Resume Analysis
        </div>

        <div class="card-text">
            Extract relevant technical and
            professional skills directly from
            your resume.
        </div>

    </div>
    """, unsafe_allow_html=True)


with c2:

    st.markdown("""
    <div class="card">

        <div class="number">02</div>

        <div class="card-title">
            Skill Gap Analysis
        </div>

        <div class="card-text">
            Compare your current skill profile
            with the requirements of your
            target job.
        </div>

    </div>
    """, unsafe_allow_html=True)


with c3:

    st.markdown("""
    <div class="card">

        <div class="number">03</div>

        <div class="card-title">
            Career Action Plan
        </div>

        <div class="card-text">
            Get focused recommendations for
            the skills that need improvement.
        </div>

    </div>
    """, unsafe_allow_html=True)


# HOW IT WORKS

st.markdown(
    '<div class="section">How it works</div>',
    unsafe_allow_html=True
)

c1, c2, c3 = st.columns(3)

with c1:

    st.markdown("""
    <div class="card">

        <div class="number">STEP 01</div>

        <div class="card-title">
            Select your role
        </div>

        <div class="card-text">
            Choose the job you want to
            prepare for.
        </div>

    </div>
    """, unsafe_allow_html=True)


with c2:

    st.markdown("""
    <div class="card">

        <div class="number">STEP 02</div>

        <div class="card-title">
            Upload resume
        </div>

        <div class="card-text">
            Upload your PDF resume for
            automatic analysis.
        </div>

    </div>
    """, unsafe_allow_html=True)


with c3:

    st.markdown("""
    <div class="card">

        <div class="number">STEP 03</div>

        <div class="card-title">
            Get your analysis
        </div>

        <div class="card-text">
            View your readiness score,
            skill gaps and recommendations.
        </div>

    </div>
    """, unsafe_allow_html=True)


# FOOTER

st.markdown("""
<div class="footer">
    Job Readiness Analyzer
    | Resume Intelligence
    | Skill Gap Analysis
    | Career Analytics
</div>
""", unsafe_allow_html=True)