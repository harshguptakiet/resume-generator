import streamlit as st
import pandas as pd
from api import generate_resume_summary  

st.set_page_config(page_title="AI Resume Builder", layout="centered")


st.sidebar.title("📂 Navigation")
page = st.sidebar.radio("Go to", ["Resume Form", "Dashboard", "ATS Checker"])


if page == "Resume Form":
    st.title("🧠 AI Resume Builder - Resume Form")

    name = st.text_input("Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")
    skills = st.text_area("Skills (comma separated)")
    experience = st.text_area("Work Experience")
    linkedin = st.text_input("linkedin")
    Github = st.text_input("github")
    Projects = st.text_area("projects")

    if st.button("Generate Resume Summary"):
        if name and skills and experience:
            with st.spinner("Generating summary..."):
                summary = generate_resume_summary(name, email, phone, skills, experience , linkedin,projects)
            st.success("✅ Your Summary:")
            st.markdown(summary)
        else:
            st.warning("Please fill all the required fields.")

# --- Dashboard Page ---
elif page == "Dashboard":
    st.title("📊 Dashboard Overview")

    # Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Resumes", "120")
    col2.metric("PDFs Generated", "98")
    col3.metric("Pending Reviews", "5")

    st.markdown("---")

    # Chart
    st.subheader("📈 Resume Processing Stats")
    data = pd.DataFrame({
        "Status": ["Uploaded", "Generated", "Pending"],
        "Count": [120, 98, 5]
    })
    st.bar_chart(data.set_index("Status"))

# --- Upload Page ---
elif page == "Upload":
    st.title("📤 Upload Resume")
    uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])

    if uploaded_file is not None:
        st.success(f"✅ '{uploaded_file.name}' uploaded successfully.")
        st.info("Processing will be added in next phase.")

# --- Footer ---
st.markdown("---")
st.caption("Internship Project — AI Resume Builder")
