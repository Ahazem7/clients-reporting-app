import streamlit as st
import logging
import os
import sys

# Add the parent directory to sys.path for module discovery
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Setup basic logging for this module only
logger = logging.getLogger(__name__)
if not logger.handlers:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

# Local imports
from app.ui.pages.dashboard_page import render_dashboard_page
from app.ui.pages.view_page import render_view_page
from app.ui.pages.inputs_page import render_inputs_page
from app.auth.auth import login_required, logout

# Streamlit logging level
logging.getLogger("streamlit").setLevel(logging.WARNING)

# Streamlit configuration
st.set_page_config(
    page_title="ESG & Shariah DataFeed Reporting",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling
st.markdown("""
<style>
    .main .block-container {padding-top: 2rem;}
    .sidebar .sidebar-content {padding-top: 2rem;}
    [data-testid="stSidebar"] {min-width: 250px;}
    h1, h2, h3 {margin-top: 0;}
    .stTabs [data-baseweb="tab-panel"] {padding-top: 1rem;}
</style>
""", unsafe_allow_html=True)

def main():
    """Main application entry point"""
    
    # Check if user is logged in, if not, show login form and exit
    if not login_required():
        return
    
    # Display welcome and logout option in sidebar
    st.sidebar.title("ESG & Shariah DataFeed")
    st.sidebar.markdown(f"Welcome, **{st.session_state.username}**")
    
    # Navigation
    pages = {
        "Dashboard": render_dashboard_page,
        "View Data": render_view_page,
        "Input Data": render_inputs_page
    }
    
    # Select page
    selection = st.sidebar.radio("Navigate", list(pages.keys()))
    
    # Display divider
    st.sidebar.divider()
    
    # Logout button
    if st.sidebar.button("Logout", type="primary"):
        logout()
        st.rerun()
    
    # Render the selected page
    try:
        pages[selection]()
    except Exception as e:
        st.error(f"Error rendering page: {str(e)}")
        logger.exception("Error rendering page")

if __name__ == "__main__":
    main() 