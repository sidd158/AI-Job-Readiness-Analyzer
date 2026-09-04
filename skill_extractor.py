import re


SKILL_KEYWORDS = {

    # Programming
    "Python": [
        "python",
        "pandas",
        "numpy",
        "scikit-learn",
        "sklearn"
    ],

    "SQL": [
        "sql",
        "mysql",
        "postgresql",
        "postgres",
        "sqlite"
    ],

    "Java": [
        "java",
        "spring",
        "spring boot"
    ],

    "JavaScript": [
        "javascript",
        "js",
        "node.js",
        "nodejs",
        "react",
        "typescript"
    ],

    "C++": [
        "c++"
    ],

    "C": [
        "c programming",
        "c language"
    ],

    # Data
    "Excel": [
        "excel",
        "microsoft excel",
        "pivot table",
        "pivot tables",
        "vlookup",
        "xlookup"
    ],

    "Power BI": [
        "power bi",
        "powerbi",
        "power query",
        "dax"
    ],

    "Tableau": [
        "tableau"
    ],

    "Data Visualization": [
        "data visualization",
        "data visualisation",
        "matplotlib",
        "seaborn",
        "plotly",
        "dashboard",
        "dashboards"
    ],

    "Statistics": [
        "statistics",
        "statistical",
        "probability",
        "hypothesis testing",
        "correlation",
        "regression"
    ],

    # AI / ML
    "Machine Learning": [
        "machine learning",
        "machine-learning",
        "scikit learn",
        "scikit-learn",
        "classification",
        "clustering",
        "regression"
    ],

    "Deep Learning": [
        "deep learning",
        "tensorflow",
        "keras",
        "pytorch",
        "neural network",
        "neural networks",
        "cnn",
        "rnn"
    ],

    "NLP": [
        "natural language processing",
        "nlp",
        "text classification",
        "sentiment analysis"
    ],

    # Web
    "HTML": [
        "html",
        "html5"
    ],

    "CSS": [
        "css",
        "css3"
    ],

    "React": [
        "react",
        "react.js",
        "reactjs"
    ],

    "Flask": [
        "flask"
    ],

    "Django": [
        "django"
    ],

    # Tools
    "Git": [
        "git",
        "github",
        "gitlab",
        "version control"
    ],

    "Docker": [
        "docker",
        "docker container",
        "containers"
    ],

    "AWS": [
        "aws",
        "amazon web services"
    ],

    "Azure": [
        "azure",
        "microsoft azure"
    ],

    # Soft skills
    "Communication": [
        "communication",
        "presentation",
        "presentations",
        "public speaking",
        "stakeholder"
    ],

    "Problem Solving": [
        "problem solving",
        "problem-solving",
        "analytical thinking",
        "critical thinking"
    ],

    "Teamwork": [
        "teamwork",
        "team work",
        "collaboration",
        "team player"
    ],

    "Leadership": [
        "leadership",
        "led a team",
        "team leader"
    ]
}


def contains_skill(text, keyword):
    """
    Check whether a keyword exists in resume text.
    """

    text = text.lower()
    keyword = keyword.lower()

    # Special handling for short terms
    if len(keyword) <= 3:
        pattern = r"(?<![a-z0-9])" + re.escape(keyword) + r"(?![a-z0-9])"
        return re.search(pattern, text) is not None

    return keyword in text


def extract_skills(text):
    """
    Extract skills from resume text.

    Returns:
        list of detected skill names
    """

    if not text:
        return []

    detected_skills = []

    for skill, keywords in SKILL_KEYWORDS.items():

        for keyword in keywords:

            if contains_skill(text, keyword):

                detected_skills.append(skill)

                break

    return sorted(set(detected_skills))


def get_skill_evidence(text):
    """
    Return detected skills with the keyword
    that caused the match.
    """

    if not text:
        return {}

    evidence = {}

    for skill, keywords in SKILL_KEYWORDS.items():

        for keyword in keywords:

            if contains_skill(text, keyword):

                evidence[skill] = keyword

                break

    return evidence


def calculate_skill_score(text, skill):
    """
    Estimate skill strength from resume evidence.

    This is an evidence score, not a true measure
    of someone's real-world ability.
    """

    if not text:
        return 0

    if skill not in SKILL_KEYWORDS:
        return 0

    matched = 0

    for keyword in SKILL_KEYWORDS[skill]:

        if contains_skill(text, keyword):
            matched += 1

    if matched == 0:
        return 0

    # Base score for mentioning a skill
    score = 50

    # Additional evidence
    score += min(matched * 10, 40)

    return min(score, 100)