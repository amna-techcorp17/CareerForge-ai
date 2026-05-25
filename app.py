import streamlit as st
import time

# --- IMPORTING YOUR BACKEND MODULES ---
from src.ai_generator import AIGenerator
from src.optimizer import CareerOptimizer
from src.docx_export import generate_docx
from src.pdf_export import generate_pdf
from src.utils import initialize_session_state

# --- PAGE CONFIG ---
st.set_page_config(page_title="CareerForge AI | Production", layout="wide")

# --- CSS INJECTION ---
st.markdown("""
    <style>
    :root {
        color-scheme: light;
        color: #0f172a;
        background-color: #f1f5f9;
        font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }

    .block-container {
        padding-top: 1.75rem !important;
        padding-bottom: 1.75rem !important;
        padding-left: 1.75rem !important;
        padding-right: 1.75rem !important;
        background: #f1f5f9;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #e2e8f0 0%, #f1f5f9 100%) !important;
        color: #0f172a !important;
        padding-top: 1.25rem !important;
        min-height: 100vh;
        border-right: none !important;
    }

    [data-testid="stSidebar"] .css-1d391kg,
    [data-testid="stSidebar"] .css-1v0mbdj,
    [data-testid="stSidebar"] .css-1q8dd3e,
    [data-testid="stSidebar"] .css-1aumxhk {
        padding-top: 0 !important;
    }

    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h4,
    [data-testid="stSidebar"] .stTextInput label,
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stFileUploader label,
    [data-testid="stSidebar"] .stRadio>div>div>label,
    [data-testid="stSidebar"] .stMarkdown>p,
    [data-testid="stSidebar"] .stMarkdown>div>p,
    [data-testid="stSidebar"] .stButton>button,
    [data-testid="stSidebar"] .stDownloadButton>button {
        color: #0f172a !important;
    }

    [data-testid="stSidebar"] .stSelectbox>div>div>div,
    [data-testid="stSidebar"] .stSelectbox>div>div>div>button,
    [data-testid="stSidebar"] .stTextInput>div>div,
    [data-testid="stSidebar"] .stTextArea>div>div,
    [data-testid="stSidebar"] .stFileUploader>div {
        background: #ffffff !important;
        border: 1px solid rgba(15, 23, 42, 0.08) !important;
        color: #0f172a !important;
    }

    [data-testid="stSidebar"] .stTextInput>div>div>input,
    [data-testid="stSidebar"] .stTextArea>div>div>textarea,
    [data-testid="stSidebar"] .stSelectbox>div>div>div>button,
    [data-testid="stSidebar"] .stSelectbox>div>div>div>div,
    [data-testid="stSidebar"] .stFileUploader>div {
        color: #0f172a !important;
    }

    [data-testid="stSidebar"] .stSelectbox>div>div>div>div,
    [data-testid="stSidebar"] .stSelectbox>div>div>div>button,
    [data-testid="stSidebar"] .stRadio>div>div>label,
    [data-testid="stSidebar"] .stRadio label {
        color: #0f172a !important;
    }

    [data-testid="stSidebar"] .css-1kyxreq,
    [data-testid="stSidebar"] .stRadio>div>div>label,
    [data-testid="stSidebar"] .stSelectbox>div>div>div>div {
        margin-bottom: 0.6rem !important;
    }

    [data-testid="stSidebar"] .stRadio>div>div>label:hover,
    [data-testid="stSidebar"] .stSelectbox>div>div>div>button:hover {
        color: #0f172a !important;
    }

    h1 {
        margin-top: 0 !important;
        color: #0f172a !important;
        font-size: 3.2rem !important;
        font-weight: 800 !important;
    }

    h2, h3, h4, h5, h6 {
        color: #0f172a !important;
        font-weight: 700 !important;
    }

    .stTextInput>div>div>input, .stTextArea>div>div>textarea,
    .stSelectbox>div>div>div>div, .stFileUploader>div {
        border: 1px solid #cbd5e1 !important;
        border-radius: 16px !important;
        background: #ffffff !important;
        box-shadow: 0 16px 40px rgba(15, 23, 42, 0.06) !important;
    }

    .stButton>button, .stDownloadButton>button {
        border-radius: 14px !important;
        border: none !important;
        background: linear-gradient(135deg, #2563eb 0%, #22c55e 100%) !important;
        color: #ffffff !important;
        padding: 0.95rem 1.5rem !important;
        box-shadow: 0 18px 45px rgba(37, 99, 235, 0.18) !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .stButton>button:hover, .stDownloadButton>button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 22px 55px rgba(37, 99, 235, 0.22) !important;
    }

    [data-testid="stExpander"] {
        border: 1px solid #cbd5e1 !important;
        border-radius: 22px !important;
        background: #ffffff !important;
        box-shadow: 0 20px 45px rgba(15, 23, 42, 0.06) !important;
        padding: 1rem 1.1rem !important;
    }

    .stMarkdown>p, .stMarkdown>div>p {
        color: #475569 !important;
    }

    .stRadio>div>div>label,
    .stSelectbox>div>div>div>div,
    .stSelectbox>div>div>div>button {
        cursor: pointer !important;
    }

    .css-1tq6sfy, .css-1v3fvcr {
        background: #ffffff !important;
        border-radius: 24px !important;
        padding: 1.4rem !important;
        box-shadow: 0 20px 58px rgba(15, 23, 42, 0.06) !important;
    }

    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stTextInput label,
    [data-testid="stSidebar"] .stTextArea label,
    [data-testid="stSidebar"] .stFileUploader label,
    [data-testid="stSidebar"] .stRadio>div>div>label {
        color: #f8fafc !important;
    }

    .stSelectbox label,
    .stTextInput label,
    .stTextArea label,
    .stFileUploader label {
        font-weight: 700 !important;
        color: #0f172a !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR NAV ---
with st.sidebar:
    st.markdown("## 🛡️ CareerForge AI")
    nav = st.radio("Portal", ["Create New Resume", "Optimize Existing Resume", "My CVs", "Login"])
    st.markdown("---")
    st.subheader("⚙️ Configuration")
    tone = st.selectbox("🎯 Tone", ["Professional", "Corporate", "Creative"])
    template = st.selectbox("📄 Template", ["Modern ATS", "Classic"])

# --- MAIN PAGE ---
st.markdown("<div style='background: linear-gradient(180deg, rgba(37,99,235,0.16), rgba(34,197,94,0.08)); border-radius: 26px; padding: 1.5rem 1.6rem; margin-bottom: 1.1rem;'>\n    <span style='font-size: 3rem;'>🚀</span>\n    <div>\n        <h1 style='margin:0; line-height:1.05;'>AI Career Assets Generator</h1>\n        <p style='margin:0.35rem 0 0; color:#64748b; font-size:1rem;'>Production-grade ATS-optimized resume and cover letter suite.</p>\n    </div>\n</div>", unsafe_allow_html=True)

# Ensure session state keys exist
initialize_session_state()


def render_ats_feedback(feedback):
    if not isinstance(feedback, dict):
        st.write(feedback)
        return
    st.markdown("#### ATS Review")
    summary = feedback.get('summary')
    if summary:
        st.write(f"**Summary:** {summary}")
    matched = feedback.get('matched', [])
    missing = feedback.get('missing', [])
    if matched:
        st.markdown("**Matched keywords:**")
        for kw in matched:
            st.write(f"- {kw}")
    if missing:
        st.markdown("**Missing keywords:**")
        for kw in missing:
            st.write(f"- {kw}")
    if not matched and not missing:
        st.info("No keyword feedback available.")

# --- LOGIC ---
if nav == "Create New Resume":
    col1, col2 = st.columns([1, 1.2], gap="large")
    with col1:
        with st.expander("👤 Personal Details", expanded=True):
            full_name = st.text_input("Full Name", key="input_full_name")
            email = st.text_input("Email", key="input_email")

        with st.expander("📞 Contact Info", expanded=True):
            linkedin = st.text_input("LinkedIn URL", key="input_linkedin")
            github = st.text_input("GitHub URL", key="input_github")
            phone = st.text_input("Phone Number", key="input_phone")
        with st.expander("🛠️ Professional Details", expanded=True):
            role = st.text_input("Target Job Role", key="input_role")
            skills = st.text_area("Skills", key="input_skills")
            jd = st.text_area("Job Description (Optional)", key="input_jd")
            experience = st.text_area("Job Experience (one entry per line)", key="input_experience")

        if st.button("Reset Form", key="reset_form"):
            st.session_state['reset_confirmation_needed'] = True

        if st.session_state.get('reset_confirmation_needed'):
            st.warning("Are you sure you want to clear the current form? This will remove all entered data and generated results.")
            c1, c2 = st.columns(2)
            with c1:
                if st.button("Confirm Reset", key="confirm_reset"):
                    keys = ['input_full_name','input_email','input_linkedin','input_github','input_phone',
                            'input_role','input_skills','input_jd','input_experience','generated','data','cover_letter','ats_jd','ats_jd_cover']
                    for k in keys:
                        if k in st.session_state:
                            del st.session_state[k]
                    st.session_state['reset_confirmation_needed'] = False
                    try:
                        if hasattr(st, 'experimental_rerun'):
                            st.experimental_rerun()
                        elif hasattr(st, 'rerun'):
                            st.rerun()
                    except Exception:
                        pass
            with c2:
                if st.button("Cancel", key="cancel_reset"):
                    st.session_state['reset_confirmation_needed'] = False

        if st.button("🚀 GENERATE ASSETS"):
            # validate required fields
            if not st.session_state.get('input_full_name') or not st.session_state.get('input_role'):
                st.error("Full Name and Target Job Role are required.")
            else:
                with st.spinner("Connecting to AI Engine..."):
                    try:
                        engine = AIGenerator()
                        resume_data = engine.generate_resume(
                            st.session_state.get('input_full_name'),
                            st.session_state.get('input_role'),
                            st.session_state.get('input_skills', ''),
                            st.session_state.get('input_jd', ''),
                            st.session_state.get('input_experience', ''),
                            st.session_state.get('input_email', ''),
                            st.session_state.get('input_linkedin', ''),
                            st.session_state.get('input_github', ''),
                            st.session_state.get('input_phone', ''),
                            tone
                        )
                        # also generate a cover letter using same inputs
                        try:
                            cover = engine.generate_cover_letter(
                                st.session_state.get('input_full_name'),
                                st.session_state.get('input_role'),
                                st.session_state.get('input_skills', ''),
                                st.session_state.get('input_jd', ''),
                                st.session_state.get('input_experience', ''),
                                tone
                            )
                            st.session_state['cover_letter'] = cover
                        except Exception:
                            st.session_state['cover_letter'] = ''
                        # store result only on success
                        st.session_state['generated'] = True
                        st.session_state['data'] = resume_data
                        # persist to user history if logged in
                        user = st.session_state.get('user')
                        if user:
                            try:
                                from src.users import save_cv
                                save_cv(user, resume_data, st.session_state.get('cover_letter', ''), metadata={'role': st.session_state.get('input_role')})
                            except Exception as e:
                                st.warning(f"Could not save to user account: {e}")
                    except Exception as e:
                        st.error(f"Generation failed: {e}")
                    finally:
                        # Some Streamlit versions do not provide experimental_rerun.
                        # Try to rerun gracefully when supported, otherwise continue.
                        try:
                            if hasattr(st, 'experimental_rerun'):
                                st.experimental_rerun()
                            elif hasattr(st, 'rerun'):
                                st.rerun()
                        except Exception:
                            # If rerun isn't available or fails, do nothing.
                            pass

    with col2:
        if st.session_state.get('generated'):
            st.markdown('<div id="generated_resume"></div>', unsafe_allow_html=True)
            st.markdown(
                """
                <script>
                const anchor = document.getElementById('generated_resume');
                if (anchor) {
                    anchor.scrollIntoView({behavior: 'smooth', block: 'start'});
                }
                </script>
                """,
                unsafe_allow_html=True,
            )
            st.success("✅ Success!")
            resume_text = st.session_state.get('data', '')
            tabs = st.tabs(["📄 AI Resume", "✉️ Cover Letter"])

            with tabs[0]:
                st.markdown("### Resume Content")
                if resume_text:
                    # Render markdown resume
                    st.markdown(resume_text)
                    st.download_button(
                        "📥 Download DOCX",
                        generate_docx(resume_text),
                        file_name="Resume.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
                    st.download_button(
                        "📥 Download PDF",
                        generate_pdf(resume_text),
                        file_name="Resume.pdf",
                        mime="application/pdf"
                    )

                    # ATS Tester
                    st.markdown("---")
                    st.markdown("### ATS Tester")
                    jd_for_test = st.text_area("Paste Job Description to test against this resume", key="ats_jd")
                    if st.button("Run ATS Test", key="ats_resume_test"):
                        if not jd_for_test:
                            st.error("Please paste a Job Description to run the ATS test.")
                        else:
                            optimizer = CareerOptimizer()
                            score, feedback = optimizer.analyze_text(resume_text, jd_for_test)
                            label = "✅ ATS Score" if score >= 80 else "⚠️ ATS Score"
                            st.metric(label, f"{score}/100")
                            if score >= 80:
                                st.success("Strong keyword alignment. Keep this resume focused and concise.")
                            elif score >= 50:
                                st.warning("Moderate alignment. Add a few more JD keywords to improve fit.")
                            else:
                                st.error("Low alignment. Add more relevant keywords from the job description.")
                            render_ats_feedback(feedback)
                else:
                    st.warning("No resume content available. Try generating again.")

            with tabs[1]:
                st.markdown("### Cover Letter")
                cover_text = st.session_state.get('cover_letter', '')
                if cover_text:
                    st.write(cover_text)
                    st.download_button(
                        "📥 Download Cover Letter (TXT)",
                        cover_text,
                        file_name="Cover_Letter.txt",
                        mime="text/plain"
                    )
                    st.download_button(
                        "📥 Download Cover Letter (PDF)",
                        generate_pdf(cover_text),
                        file_name="Cover_Letter.pdf",
                        mime="application/pdf"
                    )
                    # ATS Tester for cover letter
                    st.markdown("---")
                    st.markdown("### ATS Tester (Cover Letter)")
                    jd_for_cover_test = st.text_area("Paste Job Description to test the cover letter", key="ats_jd_cover")
                    if st.button("Run ATS Test on Cover Letter", key="ats_cover_test"):
                        if not jd_for_cover_test:
                            st.error("Please paste a Job Description to run the ATS test.")
                        else:
                            optimizer = CareerOptimizer()
                            score_c, feedback_c = optimizer.analyze_text(cover_text, jd_for_cover_test)
                            label = "✅ ATS Score (Cover Letter)" if score_c >= 80 else "⚠️ ATS Score (Cover Letter)"
                            st.metric(label, f"{score_c}/100")
                            if score_c >= 80:
                                st.success("Cover letter has strong JD alignment.")
                            elif score_c >= 50:
                                st.warning("Cover letter is okay, but add more relevant phrasing from the JD.")
                            else:
                                st.error("Cover letter needs stronger connection to the job description.")
                            render_ats_feedback(feedback_c)
                else:
                    st.info("No cover letter generated. It will appear here after successful generation.")
        else:
            st.info("👈 Fill details to generate assets.")

elif nav == "My CVs":
    st.subheader("📚 My CVs")
    user = st.session_state.get('user')
    if not user:
        st.info("Please login to view your saved CVs.")
    else:
        from src.users import load_user_data
        data = load_user_data(user) or {}
        cvs = data.get('cvs', [])
        if not cvs:
            st.info("You have no saved CVs yet. Generate one to save it to your account.")
        else:
            # show most recent first
            for idx, item in enumerate(reversed(cvs)):
                ts = item.get('timestamp')
                meta = item.get('metadata', {})
                header = f"Saved CV — {meta.get('role','') or 'No Role'} — {ts}"
                with st.expander(header, expanded=False):
                    resume_text = item.get('resume','')
                    cover_text = item.get('cover_letter','')
                    st.markdown("**Resume Preview**")
                    st.markdown(resume_text or "No resume content.")
                    c1, c2, c3 = st.columns(3)
                    with c1:
                        st.download_button("Download Resume DOCX", generate_docx(resume_text), file_name=f"resume_{idx}.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
                    with c2:
                        st.download_button("Download Resume PDF", generate_pdf(resume_text), file_name=f"resume_{idx}.pdf", mime="application/pdf")
                    with c3:
                        st.download_button("Download Resume TXT", resume_text, file_name=f"resume_{idx}.txt", mime="text/plain")

                    st.markdown("---")
                    st.markdown("**Cover Letter Preview**")
                    st.markdown(cover_text or "No cover letter.")
                    d1, d2 = st.columns(2)
                    with d1:
                        st.download_button("Download Cover TXT", cover_text, file_name=f"cover_{idx}.txt", mime="text/plain")
                    with d2:
                        st.download_button("Download Cover PDF", generate_pdf(cover_text), file_name=f"cover_{idx}.pdf", mime="application/pdf")

elif nav == "Optimize Existing Resume":
    st.subheader("📂 ATS Optimizer")
    uploaded_file = st.file_uploader("Upload PDF Resume", type=["pdf"])
    jd_opt = st.text_area("Paste Job Description")
    
    if st.button("✨ Run ATS Analysis"):
        if uploaded_file and jd_opt:
            with st.spinner("Analyzing with Optimizer..."):
                optimizer = CareerOptimizer()
                # Assuming your CareerOptimizer has this method
                score, feedback = optimizer.analyze(uploaded_file, jd_opt)
                st.metric("📊 ATS Score", f"{score}/100")
                st.write(feedback)
        else:
            st.error("Upload a resume and paste the Job Description.")

elif nav == "Login":
    st.subheader("🔑 Login")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    if st.button("Sign In", key="sign_in"):
        from src.users import verify_user
        if verify_user(username, password):
            st.success("Logged in")
            st.session_state['user'] = username
        else:
            st.error("Invalid username or password")

    with st.expander("New user? Create an account"):
        su_username = st.text_input("Choose a username", key="su_username")
        su_email = st.text_input("Email", key="su_email")
        su_password = st.text_input("Password", type="password", key="su_password")
        if st.button("Register", key="register_new_user"):
            from src.users import create_user
            if not su_username or not su_password:
                st.error("Username and password are required")
            else:
                ok = create_user(su_username, su_email, su_password)
                if ok:
                    st.success("Account created — you are now logged in.")
                    st.session_state['user'] = su_username
                else:
                    st.error("Username already exists. Choose another.")