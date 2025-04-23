import os
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pdfminer.high_level import extract_text

def extract_text_from_pdf(path):
    if hasattr(path, 'read'):  # For Streamlit uploaded file
        with open("temp_resume.pdf", "wb") as f:
            f.write(path.read())
        text = extract_text("temp_resume.pdf")
        os.remove("temp_resume.pdf")  # Clean up temp file
        return text
    else:
        return extract_text(path)

def clean_text(text):
    text = text.lower()
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text

def calculate_similarity(resume_text, jd_text):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([resume_text, jd_text])
    score = cosine_similarity(vectors[0:1], vectors[1:2])
    return round(float(score[0][0]) * 100, 2)  # in %
