import streamlit as st
import backend

st.set_page_config(page_title="Resume-To-Role – Smart Resume Analyzer & Career Matcher", layout="centered")

st.title("Resume-To-Role – Smart Resume Analyzer & Career Matcher")

st.markdown("""
Upload your resume and get personalized career role matches, skill gap analysis, and learning suggestions!
""")

# 1. Upload Resume
st.header("1. Upload Resume (PDF or Text)")
resume_file = st.file_uploader("Upload your resume", type=["pdf", "txt"])

resume_text = None
extracted = None
match_results = None

if resume_file:
    resume_text = backend.extract_resume_text(resume_file)
    st.subheader("Extracted Resume Text")
    st.code(resume_text[:1000] + ("..." if len(resume_text) > 1000 else ""))
    extracted = backend.analyze_resume_with_gemini(resume_text)
    st.success("Resume analyzed with Gemini API (mocked)")
    match_results = backend.match_roles_and_suggest_learning(extracted)

# 2. View Analysis
st.header("2. View Analysis")
if extracted:
    st.json(extracted)
    if match_results:
        st.markdown(f"**Best Matched Role:** {match_results['best_matched_role']}")
        st.markdown(f"**Match Score:** {match_results['match_score']}%")
        st.markdown(f"**Missing Skills:** {', '.join(match_results['missing_skills'])}")
else:
    st.info("Analysis results will appear here after processing your resume.")

# 3. Learning Suggestions
st.header("3. Learning Suggestions")
if match_results:
    for link in match_results["learning_suggestions"]:
        st.markdown(f"- [{link}]({link})")
else:
    st.info("Personalized learning resources will be shown here.")

# Bonus: Downloadable PDF (Placeholder)
st.markdown("**Bonus:** Save results as downloadable PDF (coming soon)")
