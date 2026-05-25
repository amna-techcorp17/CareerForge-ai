def get_resume_prompt(user_data, tone):
    return f"""
    You are an expert ATS Resume Writer. Your task is to build a professional resume using ONLY the provided user data. 
    CRITICAL RULE: Do NOT invent fake companies, fake dates, or fake universities. Use the actual details provided below.

    USER PERSONAL DETAILS:
    - Name: {user_data['full_name']}
    - Email: {user_data['email']}
    - Phone: {user_data['phone']}
    - LinkedIn: {user_data['linkedin']}
    - Portfolio/GitHub: {user_data['portfolio']}

    CAREER OBJECTIVE CONSTRAINTS:
    - Target Role: {user_data['target_role']}
    - Key Skills to Highlight: {user_data['skills']}
    - Actual Work History & Achievements: {user_data['experience']}
    - Target Job Description (Match keywords from here): {user_data['job_description']}

    WRITING STYLE DIRECTIONS:
    - Tone: {tone} (Tailor the vocabulary accordingly)
    - Output Format: Clean, beautifully structured Markdown.
    - Transform the provided raw 'Work History' into powerful, impact-driven bullet points starting with strong action verbs (e.g., Optimized, Spearheaded, Developed).
    - If specific contact links or sections are empty, omit them gracefully instead of writing placeholders like 'your_email@example.com'.
    """

def get_cover_letter_prompt(user_data, tone):
    return f"""
    Write a high-conversion cover letter for {user_data['full_name']}.
    Target Role: {user_data['target_role']}
    Tone: {tone}
    Details: {user_data['experience']}
    
    Keep it under 300 words and make it persuasive.
    """