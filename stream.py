import streamlit as st
from streamlit_option_menu import option_menu

# Import your page modules
import home
import resume
import dashboard
import ats
import auth  # Import the new auth module

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

    # --- Authentication Check ---
    # If the user is not logged in, show the auth page
    if 'user_email' not in st.session_state:
        auth.show_auth_page()
    else:
        # If logged in, show the main app
        show_main_app()

def show_main_app():
    """Renders the main application interface after login."""

    # --- Navbar ---
    selected = option_menu(
        menu_title=None,
        options=list(PAGES.keys()),
        icons=["house-door-fill", "file-earmark-person-fill", "search", "bar-chart-fill"],
        menu_icon="cast",
        default_index=0,
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

    # --- Sidebar for User Info and Logout ---
    with st.sidebar:
        st.title(f"Welcome,")
        st.write(st.session_state['user_email'])
        st.markdown("---")
        if st.button("Sign Out"):
            auth.sign_out()
            st.rerun()

    # --- Render the selected page ---
    page_function = PAGES[selected].show
    page_function()

if __name__ == "__main__":
    main()
