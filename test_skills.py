from skill_extractor import (
    extract_skills,
    get_skill_evidence,
    calculate_skill_score
)


resume_text = """
I am a B.Tech graduate with skills in Python,
SQL, Power BI, Excel and Machine Learning.

I have created data analysis dashboards using
Power BI and Excel.

I also worked with pandas, numpy and scikit-learn.

My projects include customer churn prediction
and sales data analysis.

I have good communication and problem solving skills.
"""


print("=" * 60)
print("AI JOB READINESS ANALYZER")
print("SKILL EXTRACTION TEST")
print("=" * 60)


skills = extract_skills(resume_text)

print("\nDetected Skills:")
print("-" * 60)

for skill in skills:
    print(f"[+] {skill}")


print("\nSkill Evidence:")
print("-" * 60)

evidence = get_skill_evidence(resume_text)

for skill, keyword in evidence.items():
    print(f"{skill} -> {keyword}")


print("\nSkill Scores:")
print("-" * 60)

for skill in skills:
    score = calculate_skill_score(
        resume_text,
        skill
    )

    print(f"{skill:<25} {score}%")


print("\n" + "=" * 60)