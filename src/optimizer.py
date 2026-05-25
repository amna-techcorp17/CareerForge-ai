import PyPDF2
import difflib
import re


def _tokenize(text):
    if not text:
        return []
    text = re.sub(r"[^a-z0-9\s]", " ", text.lower())
    return [t for t in text.split() if t]


class CareerOptimizer:
    def analyze(self, pdf_file, jd):
        # 1. Extract text from PDF
        reader = PyPDF2.PdfReader(pdf_file)
        resume_text = "".join([page.extract_text() or "" for page in reader.pages])
        return self.analyze_text(resume_text, jd)

    def analyze_text(self, resume_text, jd):
        """Analyze plain text resume against a job description using token and keyword overlap."""
        resume_tokens = _tokenize(resume_text)
        jd_tokens = _tokenize(jd)
        resume_set = set(resume_tokens)

        matched = []
        missing = []

        for token in sorted(set(jd_tokens), key=lambda x: jd_tokens.count(x), reverse=True):
            if token in resume_set:
                matched.append(token)
                continue

            best = max(
                (difflib.SequenceMatcher(None, token, r).ratio() for r in resume_set),
                default=0.0
            )
            if best >= 0.75:
                matched.append(token)
            else:
                missing.append(token)

        jd_unique = len(set(jd_tokens)) or 1
        score = int((len(set(matched)) / jd_unique) * 100)
        feedback = {
            'matched': sorted(set(matched))[:20],
            'missing': sorted(set(missing))[:20],
            'summary': f'Matched {len(set(matched))} of {jd_unique} JD keywords.'
        }
        return min(score, 100), feedback