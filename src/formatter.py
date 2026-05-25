import re

def clean_markdown(text):
    """Generated text se unnecessary characters aur extra spaces clean karta hai."""
    # Remove triple backticks if AI included them
    text = re.sub(r'```markdown|```', '', text)
    return text.strip()

def format_resume_header(name, role, contact_info):
    """Header ko professional styling deta hai."""
    header = f"# {name.upper()}\n"
    header += f"### {role}\n"
    header += f"{contact_info}\n"
    header += "---\n"
    return header