import streamlit as st
from streamlit_option_menu import option_menu

# Import your page modules
import home
import resume
import dashboard
import ats

# --- Page Configuration ---
st.set_page_config(
    page_title="Resumely - AI Resume Toolkit",
    page_icon="📄",
    layout="wide"
)

# A dictionary to map page names to their corresponding functions
PAGES = {
    "Home": home,
    "Resume Maker": resume,
    "ATS Checker": ats,
    "Dashboard": dashboard,
}

def main():
    """Main function to run the Streamlit app."""

    # --- Responsive Navbar ---
    # This uses the streamlit-option-menu library to create a clean navbar
    selected = option_menu(
        menu_title=None,  # required
        options=list(PAGES.keys()),  # required
        icons=["house-door-fill", "file-earmark-person-fill", "search", "bar-chart-fill"],  # optional
        menu_icon="cast",  # optional
        default_index=0,  # optional
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "#fafafa", "border-bottom": "1px solid #ddd"},
            "icon": {"color": "#6c757d", "font-size": "20px"},
            "nav-link": {
                "font-size": "16px",
                "font-weight": "600",
                "color": "#343a40",
                "text-align": "center",
                "margin": "0px 10px",
                "--hover-color": "#eee",
            },
            "nav-link-selected": {"background-color": "#00C853", "color": "white"},
        }
    )

    # --- Render the selected page ---
    page_function = PAGES[selected].show
    page_function()

if __name__ == "__main__":
    main()
