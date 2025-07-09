import streamlit as st

import resume
import dashboard
import ats









# st.title("AI Resume Builder ")

# name = st.text_input("Full Name")
# email = st.text_input("Email")
# phone = st.text_input("Phone Number")
# skills = st.text_area("Skills (comma separated)")
# experience = st.text_area("Work Experience")
# linkedin = st.text_input("linkedin")
# Github = st.text_input("github")
# Projects = st.text_area("projects")
# Education = st.text_area("Education")

# if st.button("Generate Resume Summary"):
#         if name and skills and experience:
#             with st.spinner("Generating summary..."):
#                 summary = generate_resume_summary(name, email, phone, skills, experience , linkedin,projects)
#             st.success("Your Summary:")
#             st.markdown(summary)
#         else:
#             st.warning("Please fill all the required fields.")


if "page" not in st.session_state:
    st.session_state.page = "Resume Form"
with st.sidebar:
    st.markdown("")
    if st.button("Resume maker"):
        st.session_state.page = "Resume Form"
    if st.button("Dashboard"):
        st.session_state.page = "Dashboard"
    if st.button("ATS Checker"):
        st.session_state.page = "ATS Checker"

if st.session_state.page == "Resume Form":
    resume.show()

elif st.session_state.page == "Dashboard":
    dashboard.show()

elif st.session_state.page == "ATS Checker":
    ats.show()