import streamlit as st
import pandas as pd

def show():
    st.title("📊 Dashboard")
    st.write("This is the dashboard. You can add charts or resume stats here.")


    st.title(" Dashboard Overview")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Resumes", "120")
    col2.metric("PDFs Generated", "98")
    col3.metric("Pending Reviews", "5")

    st.markdown("---")

    
    st.subheader("Resume Processing Stats")
    data = pd.DataFrame({
        "Status": ["Uploaded", "Generated", "Pending"],
        "Count": [120, 98, 5]
    })
    st.bar_chart(data.set_index("Status"))


