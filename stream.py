
import streamlit as st
from api import generate_resume_summary  # 👈 importing from api.py

st.title(" AI Resume Builder")


name = st.text_input("Full Name")
email = st.text_input("Email")
phone = st.text_input("Phone Number")
skills = st.text_area("Skills (comma separated)")
experience = st.text_area("Work Experience")




if st.button("Generate Resume Summary"):
    if name and skills and experience:
        with st.spinner("Generating summary..."):
            summary = generate_resume_summary(name, email, phone, skills, experience)
        st.success("✅ Your Summary:")
        st.markdown (summary)
        st.write(summary)
        
    else:
        st.warning("Please fill all the required fields.")
