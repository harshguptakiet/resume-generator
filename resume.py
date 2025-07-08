# import streamlit as st

# from api import generate_resume_summary  
def show():
 

 st.title("AI Resume Builder ")

 name = st.text_input("Full Name")
 email = st.text_input("Email")
 phone = st.text_input("Phone Number")
 skills = st.text_area("Skills (comma separated)")
 experience = st.text_area("Work Experience")
 linkedin = st.text_input("linkedin")
 github = st.text_input("github")
 projects = st.text_area("projects")
 Education = st.text_area("Education")

 if st.button("Generate Resume Summary"):
        if name and skills and experience:
            with st.spinner("Generating summary..."):
                summary = generate_resume_summary(name, email, phone, skills, experience , linkedin,projects , Education,github)
            st.success("Your Summary:")
            st.markdown(summary)
        else:
            st.warning("Please fill all the required fields.")

import streamlit as st
from fpdf import FPDF
from api import generate_resume_summary


# def create_resume_pdf(data):
#     pdf = FPDF()
#     pdf.add_page()
#     pdf.set_font("Arial", size=12)

#     pdf.cell(200, 10, txt="Resume", ln=True, align='C')
#     pdf.ln(10)

#     for key, value in data.items():
#         pdf.set_font("Arial", style='B', size=12)
#         pdf.cell(200, 10, txt=f"{key}:", ln=True)
#         pdf.set_font("Arial", size=12)
#         pdf.multi_cell(200, 10, txt=value)
#         pdf.ln(5)

#     return pdf.output(dest='S').encode('latin-1')

# from fpdf import FPDF




# class PDF(FPDF):
#     def header(self):
#         self.set_font("Arial", 'B', 16)
#         self.cell(0, 10, "Resume", ln=True, align='C')
#         self.ln(5)

#     def section_title(self, title):
#         self.set_font("Arial", 'B', 14)
#         self.set_text_color(0, 102, 204)
#         self.cell(0, 10, title, ln=True)
#         self.set_text_color(0, 0, 0)

#     def section_body(self, text):
#         self.set_font("Arial", size=12)
#         self.multi_cell(0, 8, text)
#         self.ln(3)

#     def section_bullet_points(self, text):
#         self.set_font("Arial", size=12)
#         for line in text.split(','):
#             self.cell(5)
#             self.cell(0, 8, f"• {line.strip()}", ln=True)
#         self.ln(3)


# def create_resume_pdf(data):
#     pdf = PDF()
#     pdf.add_page()

    
#     pdf.set_font("Arial", 'B', 12)
#     pdf.cell(0, 10, data["Name"], ln=True)
#     pdf.set_font("Arial", size=11)
#     pdf.cell(0, 8, f"Email: {data['Email']}", ln=True)
#     pdf.cell(0, 8, f"Phone: {data['Phone']}", ln=True)
#     if data['LinkedIn']:
#         pdf.cell(0, 8, f"LinkedIn: {data['LinkedIn']}", ln=True)
#     if data['GitHub']:
#         pdf.cell(0, 8, f"GitHub: {data['GitHub']}", ln=True)
#     pdf.ln(5)

    
#     if data["Summary"]:
#         pdf.section_title("Profile Summary")
#         pdf.section_body(data["Summary"])

    
#     if data["Skills"]:
#         pdf.section_title("Skills")
#         pdf.section_bullet_points(data["Skills"])

    
#     if data["Experience"]:
#         pdf.section_title("Experience")
#         pdf.section_body(data["Experience"])

    
#     if data["Projects"]:
#         pdf.section_title("Projects")
#         pdf.section_bullet_points(data["Projects"])

    
#     if data["Education"]:
#         pdf.section_title("Education")
#         pdf.section_body(data["Education"])

#     return pdf.output(dest='S').encode('latin-1')
# 

from fpdf import FPDF
import streamlit as st
from api import generate_resume_summary  # Make sure this function exists and works

def create_resume_pdf(resume_data):
    pdf = FPDF()
    pdf.add_page()

    # Add Unicode font (ensure DejaVuSans.ttf is present)
    pdf.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)
    pdf.set_font("DejaVu", "", 18)
    pdf.set_text_color(0, 0, 0)

    # Title
    pdf.cell(0, 10, resume_data["name"], ln=True)

    pdf.set_font("DejaVu", "", 12)
    pdf.cell(0, 10, f"Email: {resume_data['email']}", ln=True)
    pdf.cell(0, 10, f"Phone: {resume_data['phone']}", ln=True)
    pdf.cell(0, 10, f"LinkedIn: {resume_data['linkedin']}", ln=True)
    pdf.cell(0, 10, f"GitHub: {resume_data['github']}", ln=True)
    pdf.ln(10)

    # Skills
    pdf.set_font("DejaVu", "", 14)
    pdf.cell(0, 10, "Skills", ln=True)
    pdf.set_font("DejaVu", "", 12)
    for skill in resume_data["skills"].split(","):
        pdf.cell(0, 10, f"• {skill.strip()}", ln=True)
    pdf.ln(5)

    # Experience
    pdf.set_font("DejaVu", "", 14)
    pdf.cell(0, 10, "Experience", ln=True)
    pdf.set_font("DejaVu", "", 12)
    for exp in resume_data["experience"].split("\n"):
        pdf.multi_cell(0, 10, f"• {exp.strip()}")
    pdf.ln(5)

    # Projects
    pdf.set_font("DejaVu", "", 14)
    pdf.cell(0, 10, "Projects", ln=True)
    pdf.set_font("DejaVu", "", 12)
    for proj in resume_data["projects"].split("\n"):
        pdf.multi_cell(0, 10, f"• {proj.strip()}")
    pdf.ln(5)

    # Education
    pdf.set_font("DejaVu", "", 14)
    pdf.cell(0, 10, "Education", ln=True)
    pdf.set_font("DejaVu", "", 12)
    for edu in resume_data["education"].split("\n"):
        pdf.multi_cell(0, 10, f"• {edu.strip()}")

    return pdf.output(dest="S").encode("latin1")  # Use 'latin1' to avoid encoding errors
    

    

# def show():
#     st.title("🧠 AI Resume Builder")

#     name = st.text_input("Full Name")
#     email = st.text_input("Email")
#     phone = st.text_input("Phone Number")
#     skills = st.text_area("Skills (comma separated)")
#     experience = st.text_area("Work Experience")
#     linkedin = st.text_input("LinkedIn Profile")
#     github = st.text_input("GitHub Profile")
#     projects = st.text_area("Projects")
#     education = st.text_area("Education")
  

#     summary = st.empty()  


#     if st.button("Generate Resume Summary"):
#         if name and skills and experience:
#             with st.spinner("Generating summary..."):
#                 # summary = generate_resume_summary(
#                 #     name, email, phone, skills, experience,
#                 #     linkedin, projects, education, github
#                 # )
#                 summary = generate_resume_summary(
#     name, email, phone, skills, experience,
#     linkedin, github, projects, education  # ✅ Correct order
# )

#             st.success("Your Summary:")
#             st.markdown(summary)

#             resume_data = {
#                 "name": name,
#                 "email": email,
#                 "phone": phone,
#                 "skills": skills,
#                 "experience": experience,
#                 "linkedin": linkedin,
#                 "github": github,
#                 "projects": projects,
#                 "education": education,
#                 "summary": summary
#             }

#             # Generate PDF bytes
#             pdf_bytes = resume.create_resume_pdf(resume_data)

#             st.download_button(
#                 label="⬇️ Download Resume as PDF",
#                 data=pdf_bytes,
#                 file_name=f"{name.replace(' ', '_')}_Resume.pdf",
#                 mime="application/pdf"
#             )
#         else:
#             st.warning("Please fill all required fields.")

#             import streamlit as st
# from api import generate_resume_summary  # Import the API function

# def show():
#     st.title("🧠 AI Resume Builder - Resume Form")
#     st.markdown("Fill in your details to generate a smart resume!")

#     # 📄 Input Fields
#     name = st.text_input("Full Name")
#     email = st.text_input("Email")
#     phone = st.text_input("Phone Number")
#     linkedin = st.text_input("LinkedIn URL")
#     github = st.text_input("GitHub URL")
#     skills = st.text_area("Skills (comma-separated or in bullet form)")
#     experience = st.text_area("Work Experience")
#     projects = st.text_area("Projects")
#     education = st.text_area("Education")

#     # 🧠 Button to Generate Resume
#     if st.button("🚀 Generate Resume"):
#         # Check all fields are filled
#         if not all([name, email, phone, linkedin, github, skills, experience, projects, education]):
#             st.error("❗ Please fill in all the fields before generating the resume.")
#         else:
#             with st.spinner("Generating your resume..."):
#                 summary = generate_resume_summary(
#                     name, email, phone, skills, experience,
#                     linkedin, github, projects, education
#                 )
#                 st.success("✅ Resume generated successfully!")
#                 st.markdown(summary)

