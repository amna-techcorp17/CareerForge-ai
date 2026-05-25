import os
import re
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class ResumeScorer:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "llama-3.3-70b-versatile"

    def analyze_match(self, resume_text, job_description):
        """Resume aur JD ka mawazna karke score aur feedback deta hai."""
        
        prompt = f"""
        You are an expert Technical Recruiter and ATS Optimization Specialist.
        Analyze the following Resume against the Job Description.

        JOB DESCRIPTION:
        {job_description}

        RESUME CONTENT:
        {resume_text}

        TASK:
        1. Give an overall Match Score out of 100.
        2. Identify missing high-impact keywords.
        3. Provide 3 specific tips to improve the match.

        OUTPUT FORMAT (Strictly JSON):
        {{
            "score": int,
            "missing_keywords": [list of strings],
            "improvement_tips": [list of strings],
            "analysis_summary": "string"
        }}
        """

        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model,
                temperature=0.3, # Low temperature for consistent scoring
                response_format={"type": "json_object"}
            )
            import json
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            return {"score": 0, "error": str(e)}