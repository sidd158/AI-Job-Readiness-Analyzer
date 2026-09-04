# ============================================================
# ai_agents.py
# OPENROUTER AI AGENTS
# ============================================================

import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from openai import OpenAI


# ============================================================
# LOAD .ENV
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parent
ENV_FILE = PROJECT_DIR / ".env"

load_dotenv(
    dotenv_path=ENV_FILE,
    override=True
)


# ============================================================
# OPENROUTER CLIENT
# ============================================================

class OpenRouterAI:

    def __init__(self):

        self.api_key = os.getenv(
            "OPENROUTER_API_KEY",
            ""
        ).strip()

        self.base_url = os.getenv(
            "OPENROUTER_BASE_URL",
            "https://openrouter.ai/api/v1"
        ).strip()

        self.model = os.getenv(
            "OPENROUTER_MODEL",
            "openrouter/free"
        ).strip()

        self.client: Optional[OpenAI] = None

        if self.api_key:

            try:

                self.client = OpenAI(
                    api_key=self.api_key,
                    base_url=self.base_url,
                    default_headers={
                        "HTTP-Referer": "http://localhost:8501",
                        "X-Title": "AI Job Readiness Analyzer",
                    },
                )

            except Exception:

                self.client = None


    @property
    def available(self) -> bool:

        return (
            self.client is not None
            and bool(self.api_key)
        )


    def ask(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.3,
        max_tokens: int = 1600,
    ) -> str:

        if not self.api_key:

            return (
                "OpenRouter API key is not configured. "
                "Add OPENROUTER_API_KEY to your .env file."
            )

        if self.client is None:

            return (
                "OpenRouter client could not be initialized."
            )

        try:

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {
                        "role": "user",
                        "content": user_prompt,
                    },
                ],
                temperature=temperature,
                max_tokens=max_tokens,
            )

            if not response.choices:

                return "OpenRouter returned no response."

            content = response.choices[0].message.content

            if not content:

                return "OpenRouter returned an empty response."

            return content.strip()

        except Exception as exc:

            return f"AI request failed: {exc}"


# ============================================================
# RESUME AGENT
# ============================================================

class ResumeAgent:

    def __init__(
        self,
        ai: Optional[OpenRouterAI] = None
    ):

        self.ai = ai or OpenRouterAI()


    def run(
        self,
        resume_text: str,
        skills: List[str],
        role: str,
    ) -> str:

        system_prompt = """
You are an expert Resume Analysis Agent
for fresh graduates.

Analyze the candidate's resume for the
selected target job.

Your analysis must include:

1. Resume strengths
2. Technical skill evidence
3. Weak areas
4. Missing skills
5. Resume improvement suggestions
6. Overall hiring readiness

Rules:

- Never invent experience.
- Never invent internships.
- Never invent projects.
- Never invent certifications.
- Use only information provided in the resume.
- Keep the advice realistic for a fresher.
- Be concise and practical.

Use clear headings.
"""

        user_prompt = f"""
TARGET ROLE:
{role}

DETECTED SKILLS:
{", ".join(skills) if skills else "No skills detected"}

RESUME:
{resume_text[:12000]}
"""

        return self.ai.ask(
            system_prompt,
            user_prompt,
            temperature=0.25,
            max_tokens=1600,
        )


# ============================================================
# SKILL GAP AGENT
# ============================================================

class SkillGapAgent:

    def __init__(
        self,
        ai: Optional[OpenRouterAI] = None
    ):

        self.ai = ai or OpenRouterAI()


    def run(
        self,
        role: str,
        skill_data: List[Dict[str, Any]],
    ) -> str:

        system_prompt = """
You are a Skill Gap Analysis Agent
specializing in fresher recruitment.

Compare the candidate's current skills with
the target job requirements.

For every important gap explain:

- Skill
- Current level
- Target level
- Why it matters
- What to learn
- Practical project idea
- Priority: High, Medium or Low

Focus on skills that matter for entry-level hiring.

Do not invent candidate experience.
"""

        user_prompt = f"""
TARGET ROLE:
{role}

SKILL ANALYSIS:
{skill_data}
"""

        return self.ai.ask(
            system_prompt,
            user_prompt,
            temperature=0.25,
            max_tokens=1800,
        )


# ============================================================
# JOB MATCH AGENT
# ============================================================

class JobMatchAgent:

    def __init__(
        self,
        ai: Optional[OpenRouterAI] = None
    ):

        self.ai = ai or OpenRouterAI()


    def run(
        self,
        role: str,
        match_score: float,
        resume_text: str,
    ) -> str:

        system_prompt = """
You are a Job Matching Agent for fresh graduates.

Analyze the candidate's resume and selected
career role.

Recommend realistic entry-level or adjacent roles.

For each role include:

1. Job title
2. Why the candidate may fit
3. Important skills
4. One improvement needed

Do not invent:
- companies
- salaries
- vacancies
- current job openings
- hiring claims
"""

        user_prompt = f"""
TARGET ROLE:
{role}

CURRENT ROLE MATCH:
{match_score}%

RESUME:
{resume_text[:10000]}
"""

        return self.ai.ask(
            system_prompt,
            user_prompt,
            temperature=0.3,
            max_tokens=1400,
        )


# ============================================================
# CAREER COACH AGENT
# ============================================================

class CareerCoachAgent:

    def __init__(
        self,
        ai: Optional[OpenRouterAI] = None
    ):

        self.ai = ai or OpenRouterAI()


    def run(
        self,
        role: str,
        readiness_score: float,
        gaps: List[str],
    ) -> str:

        system_prompt = """
You are an AI Career Coach for fresh graduates.

Create a practical job-readiness roadmap.

Include:

1. Immediate actions
2. Skills to learn
3. Portfolio project
4. Resume improvements
5. Interview preparation
6. Job application strategy
7. 30-day roadmap

The plan must be realistic for a student or fresher.

Prioritize the largest skill gaps first.
"""

        user_prompt = f"""
TARGET ROLE:
{role}

READINESS SCORE:
{readiness_score}%

SKILL GAPS:
{", ".join(gaps) if gaps else "No major skill gaps"}
"""

        return self.ai.ask(
            system_prompt,
            user_prompt,
            temperature=0.35,
            max_tokens=1700,
        )


# ============================================================
# RESUME IMPROVEMENT AGENT
# ============================================================

class ResumeImprovementAgent:

    def __init__(
        self,
        ai: Optional[OpenRouterAI] = None
    ):

        self.ai = ai or OpenRouterAI()


    def run(
        self,
        role: str,
        resume_text: str,
        skills: List[str],
    ) -> str:

        system_prompt = """
You are an AI Resume Improvement Agent
specializing in fresher resumes.

Review the candidate's resume for the target role.

Analyze:

1. Professional summary
2. Technical skills
3. Projects
4. Education
5. Keywords
6. ATS readability
7. Achievement statements
8. Missing evidence

For each important issue provide:

- Problem
- Recommended change
- Example wording

Never invent qualifications, projects,
internships or achievements.

Only improve information supported by the resume.
"""

        user_prompt = f"""
TARGET ROLE:
{role}

DETECTED SKILLS:
{", ".join(skills) if skills else "None"}

RESUME:
{resume_text[:12000]}
"""

        return self.ai.ask(
            system_prompt,
            user_prompt,
            temperature=0.25,
            max_tokens=2000,
        )


# ============================================================
# INTERVIEW AGENT
# ============================================================

class InterviewAgent:

    def __init__(
        self,
        ai: Optional[OpenRouterAI] = None
    ):

        self.ai = ai or OpenRouterAI()


    def generate_questions(
        self,
        role: str,
        resume_text: str,
    ) -> str:

        system_prompt = """
You are an expert interviewer for fresher hiring.

Generate interview preparation material for
the selected target role.

Include:

- Technical questions
- Resume-based questions
- Project questions
- Behavioral questions
- HR questions

For each question provide:

1. Question
2. Strong sample answer
3. What the interviewer expects

Do not invent projects or experience.
"""

        user_prompt = f"""
TARGET ROLE:
{role}

RESUME:
{resume_text[:10000]}

Generate 10 interview questions with model answers.
"""

        return self.ai.ask(
            system_prompt,
            user_prompt,
            temperature=0.35,
            max_tokens=2800,
        )


    def evaluate_answer(
        self,
        role: str,
        question: str,
        answer: str,
    ) -> str:

        system_prompt = """
You are an expert interview evaluation agent.

Evaluate the candidate's answer as if you
were interviewing a fresher.

Provide:

1. Score out of 10
2. Strengths
3. Weaknesses
4. Missing points
5. How to improve
6. Better sample answer

Be constructive and practical.
"""

        user_prompt = f"""
ROLE:
{role}

INTERVIEW QUESTION:
{question}

CANDIDATE ANSWER:
{answer}
"""

        return self.ai.ask(
            system_prompt,
            user_prompt,
            temperature=0.25,
            max_tokens=1400,
        )


# ============================================================
# AI CAREER MANAGER
# ============================================================

class AICareerManager:

    def __init__(self):

        self.ai = OpenRouterAI()

        self.resume_agent = ResumeAgent(
            self.ai
        )

        self.skill_gap_agent = SkillGapAgent(
            self.ai
        )

        self.job_match_agent = JobMatchAgent(
            self.ai
        )

        self.career_coach_agent = CareerCoachAgent(
            self.ai
        )


    @property
    def available(self):

        return self.ai.available


    def run(
        self,
        resume_text: str,
        skills: List[str],
        role: str,
        match_score: float,
        readiness_score: float,
        gaps: List[str],
        skill_data: List[Dict[str, Any]],
    ) -> Dict[str, str]:

        results = {}

        # ----------------------------------------------------
        # RESUME AGENT
        # ----------------------------------------------------

        results["resume"] = (
            self.resume_agent.run(
                resume_text=resume_text,
                skills=skills,
                role=role,
            )
        )

        # ----------------------------------------------------
        # SKILL GAP AGENT
        # ----------------------------------------------------

        results["skill_gap"] = (
            self.skill_gap_agent.run(
                role=role,
                skill_data=skill_data,
            )
        )

        # ----------------------------------------------------
        # JOB MATCH AGENT
        # ----------------------------------------------------

        results["job_match"] = (
            self.job_match_agent.run(
                role=role,
                match_score=match_score,
                resume_text=resume_text,
            )
        )

        # ----------------------------------------------------
        # CAREER COACH
        # ----------------------------------------------------

        results["career_coach"] = (
            self.career_coach_agent.run(
                role=role,
                readiness_score=readiness_score,
                gaps=gaps,
            )
        )

        return results