import streamlit as st

def show():
    """Renders the Home Page."""

    # --- Hero Section ---
    st.title("🚀 Welcome to Resumely: Your AI-Powered Career Assistant")
    st.subheader("Build, Analyze, and Perfect Your Resume with Ease")

    st.markdown("""
    Resumely is an all-in-one toolkit designed to help you land your dream job.
    Whether you're starting from scratch or optimizing an existing resume, our suite of AI-powered tools
    will guide you every step of the way.
    """)

    # You can replace this placeholder with a real screenshot or a GIF of your app
    # Updated to use the new 'use_container_width' parameter
    st.image("https://placehold.co/800x300/00C853/FFFFFF?text=Resumely+App+Showcase", use_container_width=True)

    st.markdown("---")

    # --- Features Section ---
    st.header("✨ Our Features")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("🤖 AI Resume Builder")
        st.write("Fill out a simple form and let our AI generate a professional, polished resume tailored to your profile in seconds.")

    with col2:
        st.subheader("✅ ATS Checker")
        st.write("Upload your resume and a job description to get an instant match score. Identify missing keywords and optimize for applicant tracking systems.")

    with col3:
        st.subheader("📊 Personal Dashboard")
        st.write("Track your resume-building activities, view generation stats, and manage your documents all in one place.")

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Call to Action ---
    if st.button("Get Started with the Resume Maker"):
        # This will switch the page to the Resume Maker when clicked
        st.session_state.page = "Resume Maker"
        st.rerun()
