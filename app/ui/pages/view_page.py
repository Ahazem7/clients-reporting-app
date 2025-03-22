import streamlit as st
from app.ui.components.esg_view import render_esg_data_view, render_esg_aggregated_view
from app.ui.components.shariah_view import render_shariah_data_view, render_shariah_aggregated_view
from app.ui.components.ui_helpers import create_page_header


def render_view_page():
    """Render the data view page"""
    create_page_header("Data View", "Explore and Manage Data")
    
    # Using a session state key to track the current view section
    if "view_section" not in st.session_state:
        st.session_state["view_section"] = "ESG Data"
    
    # Radio button to select view section
    view_section = st.sidebar.radio("Select View Section", [
        "ESG Data", 
        "Shariah DataFeed Data", 
        "Aggregated Reports"
    ], key="view_section_radio")
    
    # Update session state when view changes
    if view_section != st.session_state["view_section"]:
        st.session_state["view_section"] = view_section
    
    # Clear section-specific filter states when changing sections
    if view_section == "ESG Data":
        # Don't reset filters within the section
        render_esg_data_view()
    elif view_section == "Shariah DataFeed Data":
        # Don't reset filters within the section
        render_shariah_data_view()
    elif view_section == "Aggregated Reports":
        st.subheader("Aggregated Data Reports")
        
        report_section = st.radio("Select report type", [
            "ESG Aggregated Data", 
            "Shariah DataFeed Aggregated Data"
        ], key="aggregated_report_type")
        
        if report_section == "ESG Aggregated Data":
            render_esg_aggregated_view()
        elif report_section == "Shariah DataFeed Aggregated Data":
            render_shariah_aggregated_view() 