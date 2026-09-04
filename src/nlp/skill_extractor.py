import re


# ============================================================
# AI JOB READINESS ANALYZER
# NLP SKILL EXTRACTOR
# ============================================================


SKILLS = {

    "python": [
        "python"
    ],

    "sql": [
        "sql",
        "mysql",
        "postgresql",
        "postgres"
    ],

    "excel": [
        "excel",
        "microsoft excel",
        "ms excel"
    ],

    "power_bi": [
        "power bi",
        "powerbi"
    ],

    "statistics": [
        "statistics",
        "statistical analysis",
        "statistical modeling"
    ],

    "machine_learning": [
        "machine learning",
        "machine-learning",
        "ml"
    ],

    "tableau": [
        "tableau"
    ],

    "communication": [
        "communication",
        "communication skills"
    ],

    "git": [
        "git",
        "github",
        "gitlab"
    ],

    "data_visualization": [
        "data visualization",
        "data visualisation",
        "data visualization tools"
    ],

    "numpy": [
        "numpy"
    ],

    "pandas": [
        "pandas"
    ],

    "scikit_learn": [
        "scikit-learn",
        "scikit learn",
        "sklearn"
    ],

    "tensorflow": [
        "tensorflow"
    ],

    "pytorch": [
        "pytorch"
    ],

    "java": [
        "java"
    ],

    "c++": [
        "c++"
    ],

    "html": [
        "html"
    ],

    "css": [
        "css"
    ],

    "javascript": [
        "javascript",
        "java script"
    ]
}


def clean_text(text):
    """
    Basic text cleaning.
    """

    if not isinstance(text, str):
        return ""

    text = text.lower()

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def skill_exists(text, keyword):
    """
    Check whether a keyword exists as a word/phrase.
    """

    pattern = (
        r"(?<![a-zA-Z0-9])"
        + re.escape(keyword.lower())
        + r"(?![a-zA-Z0-9])"
    )

    return bool(
        re.search(
            pattern,
            text
        )
    )


def extract_skills(text):
    """
    Extract skills from resume text.
    """

    text = clean_text(text)

    found_skills = []

    for skill, keywords in SKILLS.items():

        for keyword in keywords:

            if skill_exists(
                text,
                keyword
            ):

                found_skills.append(skill)

                break

    return sorted(
        set(found_skills)
    )


def create_skill_vector(text):
    """
    Convert extracted skills into a binary vector.
    """

    found_skills = extract_skills(text)

    vector = {}

    for skill in SKILLS:

        vector[skill] = (
            1
            if skill in found_skills
            else 0
        )

    return vector


if __name__ == "__main__":

    sample_resume = """
    B.Tech Computer Science graduate.

    Skills:
    Python, SQL, Excel, Power BI,
    Pandas, NumPy, Machine Learning,
    Statistics, Git and Tableau.

    Projects:
    Customer Churn Prediction
    Sales Dashboard
    """

    print("=" * 60)
    print("NLP SKILL EXTRACTION TEST")
    print("=" * 60)

    skills = extract_skills(
        sample_resume
    )

    print("\nDetected Skills:")

    for skill in skills:
        print("✓", skill)

    print("\nSkill Vector:")

    vector = create_skill_vector(
        sample_resume
    )

    for skill, value in vector.items():

        print(
            f"{skill:20} : {value}"
        )