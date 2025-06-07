import streamlit as st
import backend
from PIL import Image

st.set_page_config(page_title="Resume-To-Role – Smart Resume Analyzer & Career Matcher", layout="centered", page_icon="🧑‍💼")

# --- Sidebar Branding ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=80)
st.sidebar.title("Resume-To-Role")
st.sidebar.markdown("""
**Smart Resume Analyzer & Skill Uplifter**

Built for Google GenAI Hackathon
""")

st.sidebar.header("AI Engine")
use_gemini = st.sidebar.checkbox("Use Google Gemini/Vertex AI (Demo Mode)", value=False)

# --- Main Title ---
st.markdown("""
<style>
.big-title {font-size:2.5rem; font-weight:700; color:#2E86C1; letter-spacing:1px;}
.sub-title {font-size:1.2rem; color:#34495E;}
.card {background:#F4F6F7; border-radius:12px; padding:1.5em 1em; margin-bottom:1.5em; box-shadow:0 2px 8px #0001;}
.skill-pill {display:inline-block; background:#D6EAF8; color:#154360; border-radius:20px; padding:0.3em 1em; margin:0.2em 0.3em; font-weight:500;}
.coursera-link {color:#2874A6; font-weight:600;}
</style>
<div class='big-title'>🧑‍💼 Resume-To-Role</div>
<div class='sub-title'>Upload your resume to discover your key skills and get personalized learning resources powered by AI!</div>
""", unsafe_allow_html=True)

# --- Upload Resume ---
st.markdown("""
---
### 1. Upload Resume (PDF or Text)
""")
resume_file = st.file_uploader("Upload your resume", type=["pdf", "txt"])

resume_text = None
results = None

if resume_file:
    resume_text = backend.extract_resume_text(resume_file)
    with st.expander("See Extracted Resume Text", expanded=False):
        st.code(resume_text[:2000] + ("..." if len(resume_text) > 2000 else ""))
    results = backend.extract_skills_and_suggest_courses(resume_text, use_gemini=use_gemini)
    st.success(f"Resume analyzed with: {results.get('source', 'Local')}")

# --- Results Section ---
st.markdown("""
---
### 2. Extracted Skills & Learning Resources
""")

if results:
    if results["extracted_skills"]:
        # --- Skills Card ---
        st.markdown("<div class='card'><b>Extracted Skills:</b><br>" +
            " ".join([f"<span class='skill-pill'>{skill}</span>" for skill in results["extracted_skills"]]) +
            "</div>", unsafe_allow_html=True)
        # --- Learning Resources ---
        st.markdown("<div class='card'><b>Learning Resources for Your Skills:</b></div>", unsafe_allow_html=True)
        cols = st.columns(2)
        for idx, (skill, links) in enumerate(results["course_links"].items()):
            with cols[idx % 2]:
                st.markdown(
                    f"<span class='skill-pill'>{skill}</span> "
                    f"<a class='coursera-link' href='{links['Coursera']}' target='_blank'>🔗 Coursera</a> | "
                    f"<a class='coursera-link' href='{links['Udemy']}' target='_blank' style='color:#E67E22;'>🎓 Udemy</a>",
                    unsafe_allow_html=True
                )
    else:
        st.info("No recognized skills found in the resume.")
else:
    st.info("Analysis results will appear here after processing your resume.")
