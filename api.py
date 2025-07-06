# api.py
import streamlit as st
import google.generativeai as genai

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
for model in genai.list_models():
    print(model.name)

def generate_resume_summary(name, email, phone, skills, experience):
    prompt = f"""
  
Create a professional resume using the details below. Include the following sections in the output:

1. Full Name
2. Contact (Email and Phone)
3. Skills (as bullet points)
4. Experience (as bullet points or brief lines)
5. Summary (3–4 line intro at the top)

Name: {name}
Email: {email}
Phone: {phone}
Skills: {skills}
Experience: {experience}

Format the resume cleanly using markdown.
"""


    model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")  # or "models/gemini-pro"


    response = model.generate_content(prompt)
    return response.text.strip()
