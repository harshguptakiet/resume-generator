# import streamlit as st
# import google.generativeai as genai

# genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
# for model in genai.list_models():
#     print(model.name)

# # def generate_resume_summary(name, email, phone, skills, experience , linkedin , github , projects, education, ):
# #     prompt = f"""
# def generate_resume_summary(
#     name, email, phone, skills, experience,
#     linkedin, github, projects, education
# ):
#    prompt = f"""
  
# Create a professional resume using the details below. Include the following sections in the output:

# 1. Full Name
# 2. Contact (Email and Phone)
# 3. Skills (as bullet points)
# 4. Experience (as bullet points or brief lines)
# 5. Summary (3–4 line intro at the top)

# Name: {name}
# Email: {email}
# Phone: {phone}
# Skills: {skills}
# Experience: {experience}
# linkedin: {linkedin}
# Github: {github}
# Projects : {projects}
# Education :{education}


# Format the resume cleanly using markdown.
# """


# def generate_resume_summary(prompt):
#     model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
#     response = model.generate_content(prompt)
#     return response.text.strip()


import streamlit as st
import google.generativeai as genai

# Configure Gemini API key securely from Streamlit secrets
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

def generate_resume_summary(
    name, email, phone, skills, experience,
    linkedin, github, projects, education
):
    # Prompt to generate resume
    prompt = f"""
Create a professional resume using the details below. Include the following sections in the output:

1. Full Name
2. Contact (Email and Phone)
3. Skills (as bullet points)
4. Experience (as bullet points or brief lines)
5. Summary (3–4 line intro at the top)
6. Projects and Education

Name: {name}
Email: {email}
Phone: {phone}
Skills: {skills}
Experience: {experience}
LinkedIn: {linkedin}
GitHub: {github}
Projects: {projects}
Education: {education}

Format the resume cleanly using markdown.
"""

    model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text.strip()
