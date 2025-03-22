import streamlit as st
import hashlib
import logging

logger = logging.getLogger(__name__)

# Default credentials - in a real app, these would be stored securely, hashed, and not in source code
DEFAULT_USERNAME = "IR_test"
DEFAULT_PASSWORD = "IR2025test"

def check_password(username, password):
    """
    Check if username and password match the default credentials
    
    Args:
        username (str): Username to check
        password (str): Password to check
        
    Returns:
        bool: True if credentials are valid, False otherwise
    """
    return username == DEFAULT_USERNAME and password == DEFAULT_PASSWORD

def login_required():
    """
    Require login to access the app. 
    Shows a login form if not logged in, otherwise returns True.
    
    Returns:
        bool: True if user is authenticated, False otherwise
    """
    # Initialize session state
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.failed_login = False
    
    # If already authenticated, we're done
    if st.session_state.authenticated:
        return True
    
    # Show login form in a container
    st.markdown("<h1 style='text-align: center;'>ESG & Shariah DataFeed Reporting</h1>", unsafe_allow_html=True)
    
    login_container = st.container()
    login_container.markdown("<h2 style='text-align: center;'>Login</h2>", unsafe_allow_html=True)
    
    # Center the login form
    col1, col2, col3 = login_container.columns([1, 2, 1])
    
    with col2:
        # Create form with username and password inputs
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login", use_container_width=True)
            
            if st.session_state.failed_login:
                st.error("Invalid username or password. Please try again.")
            
            if submit:
                if check_password(username, password):
                    logger.info(f"Successful login: {username}")
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.session_state.failed_login = False
                    st.rerun()
                else:
                    logger.warning(f"Failed login attempt: {username}")
                    st.session_state.failed_login = True
                    st.error("Invalid username or password. Please try again.")
    
    # Show some information about the app
    login_container.markdown("""
    <div style='text-align: center;'>
        <p>Welcome to the ESG & Shariah DataFeed Reporting application.</p>
        <p>Please login with your credentials to access the application.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Add a footer
    st.markdown("""
    <div style='position: fixed; bottom: 0; width: 100%; text-align: center; padding: 10px; background-color: #f0f2f6;'>
        <p>© 2025 - ESG & Shariah DataFeed Reporting</p>
    </div>
    """, unsafe_allow_html=True)
    
    # User is not authenticated
    return False

def logout():
    """Log out the current user by resetting session state"""
    if 'authenticated' in st.session_state:
        st.session_state.authenticated = False
    if 'username' in st.session_state:
        del st.session_state.username 