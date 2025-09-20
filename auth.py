import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth

from database import create_user_profile_if_not_exists # Import the new database function

import re  


# --- Firebase Initialization ---
try:
    if not firebase_admin._apps:
        cred = credentials.Certificate(dict(st.secrets["firebase_credentials"]))
        firebase_admin.initialize_app(cred)
    FIREBASE_AVAILABLE = True
except Exception as e:
    print(f"Firebase not available: {e}")
    FIREBASE_AVAILABLE = False

# --- Email Format Validator ---
def is_valid_email(email):
    # Enforce at least 2 characters before the @ and a valid domain
    pattern = r'^(?!.*[.]{2})[a-zA-Z0-9](\.?[a-zA-Z0-9_-])*@[a-zA-Z0-9-]+(\.[a-zA-Z]{2,})+$'
    return re.match(pattern, email) is not None

# --- Authentication Functions ---

def sign_up(email, password):
    """Creates a new user in Firebase Auth and a corresponding profile in Firestore."""
    if not FIREBASE_AVAILABLE:
        st.error("🔒 Authentication features require Firebase setup. Please follow the Firebase Setup Guide.")
        return False
    
    try:
        user = auth.create_user(email=email, password=password)
        # Create a profile in Firestore for the new user, which now includes a default name
        create_user_profile_if_not_exists(user.uid, user.email)
        st.success(f"Account created successfully for {user.email}! Please proceed to the Sign In tab.")
        return True
    except auth.EmailAlreadyExistsError:
        st.error("An account with this email already exists. Please try signing in instead.")
        return False
    except Exception as e:
        error_message = str(e)
        if "CONFIGURATION_NOT_FOUND" in error_message:
            st.error("🚨 **Firebase Authentication Setup Required**")
            st.info("""
            **To enable user accounts, please complete these steps:**
            
            1. Go to [Firebase Console](https://console.firebase.google.com/)
            2. Select your project: `resume-4036a`
            3. Click **Authentication** → **Get started**
            4. Go to **Sign-in method** tab
            5. Enable **Email/Password** provider
            6. Also enable **Firestore Database** if not already done
            
            Until then, you can still use all other features without signing in!
            """)
        else:
            st.error(f"Error creating account: {error_message}")
        return False

def sign_in(email, password):
    """Signs in a user and stores their email and UID in the session state."""
    if not FIREBASE_AVAILABLE:
        st.error("🔒 Authentication features require Firebase setup. Please follow the Firebase Setup Guide.")
        return False
    
    try:
        user = auth.get_user_by_email(email)


        st.session_state['user_email'] = user.email
        st.session_state['uid'] = user.uid # Store the user's unique ID
        
        # Ensure a profile exists, useful for users created before this feature was added
        create_user_profile_if_not_exists(user.uid, user.email)
        return True
    except Exception as e:
        st.error(f"Error signing in: Invalid email or password.")
        return False

def sign_out():
    """Signs out the current user by clearing the session state."""
    if 'user_email' in st.session_state:
        del st.session_state['user_email']
    if 'uid' in st.session_state:
        del st.session_state['uid']
    st.success("You have been signed out.")

def show_auth_page():
    """Renders the unified Sign In / Sign Up page using tabs."""
    st.title("Welcome to Resumely")
    
    if not FIREBASE_AVAILABLE:
        st.warning("🔧 **Firebase Setup Required**: Authentication features are currently unavailable. Please follow the [Firebase Setup Guide](FIREBASE_SETUP.md) to enable user accounts.")
        st.info("💡 **Good News**: You can still use the Resume Builder, ATS Checker, and other features without signing in!")
        return
    
    # Check if Firebase Authentication is properly configured
    st.info("🔐 **User Account Features Available** - Sign in or create an account to save your resumes and preferences!")
    
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        signin_tab, signup_tab = st.tabs(["**Sign In**", "**Sign Up**"])
        with signin_tab:
            with st.form("signin_form", clear_on_submit=True):
                email = st.text_input("Email", key="signin_email")
                password = st.text_input("Password", type="password", key="signin_password")
                signin_submitted = st.form_submit_button("Sign In", use_container_width=True)

            if signin_submitted and email and password and sign_in(email, password):
                st.rerun()


            if signin_submitted:
                if email and password:
                    if sign_in(email, password):
                        st.rerun()
                else:
                    st.warning("Please enter both email and password.")

        with signup_tab:
            with st.form("signup_form", clear_on_submit=True):
                new_email = st.text_input("Email", key="signup_email")
                new_password = st.text_input("Password", type="password", key="signup_password")
                confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm_password")
                signup_submitted = st.form_submit_button("Create Account", use_container_width=True)

            if signup_submitted and new_email and new_password and confirm_password:
                if new_password == confirm_password:
                    sign_up(new_email, new_password)


            if signup_submitted:
                if new_email and new_password and confirm_password:
                    if not is_valid_email(new_email):
                        st.error("Invalid email format. Please enter a valid email address.")
                    elif new_password != confirm_password:
                        st.error("Passwords do not match.")
                    else:
                        sign_up(new_email, new_password)

                else:
                    st.error("Passwords do not match.")
