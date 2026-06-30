import re
from typing import Any, Dict


class JobParser:
    @staticmethod
    def parse(job_description: str) -> Dict[str, Any]:
        jd_clean = job_description.strip()
        jd_lower = jd_clean.lower()

        # Validation for meaningless strings
        if len(jd_clean) < 20 or len(jd_clean.split()) < 5:
            return {
                "role": "Unknown",
                "summary": "Unknown",
                "core_skills": [],
                "nice_to_have": [],
                "required_experience": "Not Specified",
                "keywords": [],
                "confidence_score": 0.0,
                "validation_warning": "Job description is too short or meaningless.",
            }

        skills_keywords = [
            "python",
            "machine learning",
            "pytorch",
            "react",
            "typescript",
            "sql",
            "docker",
            "kubernetes",
            "aws",
            "ci/cd",
            "data science",
            "devops",
            "java",
            "c++",
            "go",
            "ruby",
            "node.js",
            "frontend",
            "backend",
            "full stack",
            "cloud",
            "security",
            "ai",
            "deep learning",
        ]

        core_skills = []
        for s in skills_keywords:
            if re.search(r"\b" + re.escape(s) + r"\b", jd_lower):
                core_skills.append(
                    s.title() if s not in ["aws", "ci/cd", "sql", "ai"] else s.upper()
                )

        nice_to_have_keywords = [
            "agile",
            "scrum",
            "communication",
            "leadership",
            "mentoring",
            "teamwork",
            "collaboration",
        ]

        found_nice = []
        for s in nice_to_have_keywords:
            if re.search(r"\b" + re.escape(s) + r"\b", jd_lower):
                found_nice.append(s.title())

        # Role inference using strict regex checks
        role = "Unknown"
        if (
            re.search(r"\b(machine learning|ml)\b", jd_lower)
            or re.search(r"\bai\b", jd_lower)
            and "engineer" in jd_lower
        ):
            role = "Machine Learning Engineer"
        elif re.search(r"\b(devops|sre)\b", jd_lower):
            role = "DevOps Engineer"
        elif "data scientist" in jd_lower:
            role = "Data Scientist"
        elif "research" in jd_lower and (
            "ai" in jd_lower or "machine learning" in jd_lower
        ):
            role = "AI Research Engineer"
        elif "backend" in jd_lower:
            role = "Backend Engineer"
        elif "frontend" in jd_lower:
            role = "Frontend Engineer"
        elif "full stack" in jd_lower or "fullstack" in jd_lower:
            role = "Full Stack Engineer"
        elif "cloud" in jd_lower:
            role = "Cloud Engineer"
        elif "security" in jd_lower:
            role = "Security Engineer"
        elif "software engineer" in jd_lower or "developer" in jd_lower:
            role = "Software Engineer"

        # Experience
        exp_match = re.search(r"(\d+)(?:\+|-)?\s*(?:to\s*\d+\s*)?years?", jd_lower)
        experience = f"{exp_match.group(1)}+ years" if exp_match else "Not Specified"

        # Summary extraction (first valid sentence > 10 chars)
        sentences = [
            s.strip() for s in re.split(r"[.!?\n]", jd_clean) if len(s.strip()) > 10
        ]
        summary = sentences[0] + "." if sentences else "Unknown"

        # Confidence calculation based on extracted data
        confidence = 0.0
        if role != "Unknown":
            confidence += 0.4
        if experience != "Not Specified":
            confidence += 0.2
        if core_skills:
            confidence += min(0.3, len(core_skills) * 0.05)
        if len(jd_clean) > 200:
            confidence += 0.1

        confidence = round(min(1.0, confidence), 2)
        warning = None
        if confidence < 0.5:
            warning = "Low confidence in parsed data. Please provide a more detailed job description."

        return {
            "role": role,
            "summary": summary,
            "core_skills": core_skills,
            "nice_to_have": found_nice,
            "required_experience": experience,
            "keywords": ([role] if role != "Unknown" else []) + core_skills,
            "confidence_score": confidence,
            "validation_warning": warning,
        }
