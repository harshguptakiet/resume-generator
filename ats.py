import streamlit as st

def show():
    # st.title("✅ ATS Checker")
    # st.write("Upload your resume to check ATS compatibility.")
    # uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx"])
      import streamlit as st
import docx2txt
import PyPDF2
import re
from io import StringIO


def extract_text_from_resume(uploaded_file):
    text = ""
    if uploaded_file is not None:
        if uploaded_file.type == "application/pdf":
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            for page in pdf_reader.pages:
                text += page.extract_text()
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            text = docx2txt.process(uploaded_file)
        else:
            st.warning("Only PDF or DOCX files are supported.")
    return text


def keyword_match_score(resume_text, job_description):
    resume_words = set(re.findall(r'\b\w+\b', resume_text.lower()))
    job_words = set(re.findall(r'\b\w+\b', job_description.lower()))
    matched_keywords = resume_words & job_words
    score = len(matched_keywords) / len(job_words) * 100 if job_words else 0
    return round(score, 2), matched_keywords



def show():
    st.title("ATS Resume Checker")
    st.write("Upload your resume and paste the job description to get a match score.")

    uploaded_file = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"])
    job_description = st.text_area("Paste the Job Description Here")

    if uploaded_file and job_description:
        with st.spinner("Analyzing resume..."):
            resume_text = extract_text_from_resume(uploaded_file)
            score, matched_keywords = keyword_match_score(resume_text, job_description)

            st.success(f"Match Score: {score}%")
            st.write(f" Matched Keywords: {', '.join(sorted(matched_keywords))}")

            if score < 50:
                st.warning("Your resume may not be optimized for this job. Try to include more relevant skills and keywords.")
            else:
                st.success("Your resume seems well-tailored for this role!")

