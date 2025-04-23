import streamlit as st 
import os
from utils import extract_text_from_pdf, clean_text, calculate_similarity

st.set_page_config(page_title="Resume Screener", layout="wide")

# Sidebar
with st.sidebar:
    st.title("🔧 Options")
    st.markdown("Built with ❤️ using NLP & Streamlit")
    st.markdown("[GitHub Repo](https://github.com/your-repo)")  # <-- replace with your actual repo

# Title & Description
st.title("📄 AI Resume Screener using NLP")
st.markdown("""
This app compares uploaded resumes against a job description and gives a **matching score**.  
It also highlights resumes that may need improvements based on missing skills or keywords.
""")

# Load Job Description
try:
    with open("job_description.txt", "r", encoding='utf-8') as f:
        jd_raw = f.read()
    jd_clean = clean_text(jd_raw)
except FileNotFoundError:
    st.error("🚫 Job description file not found. Please ensure 'job_description.txt' is in the app folder.")
    st.stop()

st.subheader("📌 Job Description")
st.info(jd_raw)

# Resume Upload
st.subheader("📤 Upload Resumes")
uploaded_files = st.file_uploader("Upload multiple resumes (PDF)", type=["pdf"], accept_multiple_files=True)

if uploaded_files:
    st.subheader("📊 Resume Match Results")
    results = []

    for uploaded_file in uploaded_files:
        resume_name = uploaded_file.name
        resume_text = extract_text_from_pdf(uploaded_file)
        resume_clean = clean_text(resume_text)
        match_score = calculate_similarity(resume_clean, jd_clean)

        # Simple keyword gap finder
        missing_keywords = []
        for word in jd_clean.split():
            if word not in resume_clean and len(word) > 5:  # basic filtering
                missing_keywords.append(word)
        keyword_hint = ", ".join(missing_keywords[:5]) if match_score < 70 else ""

        result = {
            "Resume": resume_name,
            "Score": match_score,
            "Recommendation": "✅ Strong Match" if match_score >= 70 else "⚠️ Needs Improvement",
            "Hint": keyword_hint
        }

        results.append(result)

    # Display Results
    for res in results:
        st.write(f"**{res['Resume']}** - Match Score: **{res['Score']}%** → {res['Recommendation']}")
        st.progress(int(res['Score']))
        if res['Hint']:
            st.markdown(f"🔍 Might be missing important terms: `{res['Hint']}`")
        st.markdown("---")

else:
    st.warning("Please upload at least one resume to begin screening.")
