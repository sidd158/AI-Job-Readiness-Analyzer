# ============================================================
# AI JOB READINESS ANALYZER
# JOB REQUIREMENTS
# ============================================================

JOB_REQUIREMENTS = {

    "Data Analyst": [
        "python",
        "sql",
        "excel",
        "power_bi",
        "statistics",
        "data_visualization",
        "communication",
        "git"
    ],

    "Data Scientist": [
        "python",
        "sql",
        "statistics",
        "machine_learning",
        "pandas",
        "numpy",
        "scikit_learn",
        "data_visualization",
        "git"
    ],

    "Business Analyst": [
        "excel",
        "sql",
        "power_bi",
        "statistics",
        "communication",
        "data_visualization"
    ],

    "Python Developer": [
        "python",
        "sql",
        "git",
        "html",
        "css",
        "javascript"
    ],

    "ML Engineer": [
        "python",
        "sql",
        "machine_learning",
        "scikit_learn",
        "tensorflow",
        "pytorch",
        "numpy",
        "pandas",
        "git"
    ]
}


def get_job_requirements(job_role):

    if job_role not in JOB_REQUIREMENTS:

        raise ValueError(
            f"Unknown job role: {job_role}"
        )

    return JOB_REQUIREMENTS[job_role]


def get_all_job_roles():

    return list(JOB_REQUIREMENTS.keys())


if __name__ == "__main__":

    print("=" * 60)
    print("JOB REQUIREMENTS")
    print("=" * 60)

    for role, skills in JOB_REQUIREMENTS.items():

        print(f"\n{role}")

        for skill in skills:

            print(f"  ✓ {skill}")