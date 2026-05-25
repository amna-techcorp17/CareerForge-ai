from groq import Groq
from dotenv import load_dotenv
import os
import re

load_dotenv()

class AIGenerator:
    def __init__(self):
        self.client = Groq(
            api_key=os.getenv("GROQ_API_KEY")
        )
        self.model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
    def generate_resume(self, full_name, role, skills, jd, experience="", email="", linkedin="", github="", phone="", tone="Professional"):
        """Generate a Markdown-formatted resume using only the provided fields.

        Important: do NOT invent contact details, phone numbers, links, or job
        experience that the user did not provide. If a field is empty, write
        'Not provided' for that field.
        """

        safe_full_name = (full_name or "Not provided").strip()
        safe_role = (role or "Not provided").strip()
        safe_skills = (skills or "Not provided").strip()
        safe_jd = (jd or "Not provided").strip()
        safe_experience = (experience or "Not provided").strip()
        safe_email = (email or "Not provided").strip()
        safe_linkedin = (linkedin or "Not provided").strip()
        safe_github = (github or "Not provided").strip()
        safe_phone = (phone or "Not provided").strip()

        def build_skill_lines(skill_text: str):
            if skill_text.lower() == "not provided" or not skill_text.strip():
                return ["- Not provided"]
            items = re.split(r"[\n,;]+", skill_text)
            bullets = [f"- {item.strip()}" for item in items if item.strip()]
            return bullets or ["- Not provided"]

        skill_lines = build_skill_lines(safe_skills)
        experience_section = safe_experience if safe_experience.lower() != "not provided" else "No professional experience details provided yet."
        if experience_section != "No professional experience details provided yet.":
            exp_items = [line.strip() for line in re.split(r"[\n;]+", experience_section) if line.strip()]
            if exp_items:
                experience_section = "\n".join(f"- {item}" for item in exp_items)

        prompt = f"""
    You are a professional resume assistant. Write only a polished professional summary and an optional experience bullet list using the provided information. Use a confident, factual tone and do not invent any details.

    Tone: {tone}

    Target Role: {safe_role}
    Skills: {safe_skills}
    Job Description: {safe_jd}
    Experience: {safe_experience}

    Output exactly two sections in Markdown: "Summary" and "Experience".
    - Summary: one paragraph, ATS-friendly, using the role and skills.
    - Experience: if experience is provided, return bullet points based on the input lines; otherwise say "No professional experience details provided yet."
    """

        chat_completion = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=self.model
        )

        ai_body = chat_completion.choices[0].message.content.strip()
        summary_part = ai_body
        experience_part = ""
        if "Experience:" in ai_body:
            summary_part, experience_part = ai_body.split("Experience:", 1)
        summary_part = re.sub(r"(?i)^\s*(#+\s*)?Summary[:\s]*", "", summary_part).strip()
        experience_part = experience_part.strip()
        experience_part = re.sub(r"(?im)^\s*(#+\s*)?Experience[:\s]*\n?", "", experience_part).strip()

        resume_text = (
            f"## {safe_full_name}\n\n"
            f"**Target Role:** {safe_role}\n\n"
            f"### Contact Information\n"
            f"- Email: {safe_email}\n"
            f"- LinkedIn: {safe_linkedin}\n"
            f"- GitHub: {safe_github}\n"
            f"- Phone: {safe_phone}\n\n"
            f"### Professional Summary\n"
            f"{summary_part}\n\n"
            f"### Experience\n"
        )

        if experience_part:
            resume_text += experience_part + "\n\n"
        elif experience_section.lower().startswith("no professional experience details"):
            resume_text += experience_section + "\n\n"
        else:
            resume_text += experience_section + "\n\n"

        resume_text += "### Skills\n" + "\n".join(skill_lines)
        return resume_text

    def generate_cover_letter(self, full_name, role, skills, jd, experience="", tone="Professional"):
        """Generate a short professional cover letter tailored to the role and JD.

        The model must not invent contact details or additional experiences.
        Use only the provided fields.
        """
        safe_full_name = full_name or "Not provided"
        safe_role = role or "Not provided"
        safe_skills = skills or "Not provided"
        safe_jd = jd or "Not provided"
        safe_experience = experience or "Not provided"

        prompt = f"""
    You are a professional career assistant. Write a concise, one-page cover letter in Markdown for the candidate below applying to the target role.
    Use only the information provided — do NOT invent contact details, dates, or additional experience.
    If information is missing, acknowledge it as 'Not provided'. If a field is present, use it exactly as provided.

    Tone: {tone}

    Name: {safe_full_name}
    Target Role: {safe_role}
    Skills: {safe_skills}
    Job Description: {safe_jd}
    Experience: {safe_experience}

    Structure the letter with a professional opening, one or two achievement-focused paragraphs, and a respectful closing.
    Keep the tone confident and factual, without inventing any details.
    """

        chat_completion = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=self.model
        )

        return chat_completion.choices[0].message.content