import streamlit as st
from app.ui.components.esg_view import render_esg_data_view, render_esg_aggregated_view
from app.ui.components.shariah_view import render_shariah_data_view, render_shariah_aggregated_view
from app.ui.components.ui_helpers import create_page_header


def render_view_page():
    """Render the data view page"""
    create_page_header("Data View", "Explore and Manage Data")
    
    view_section = st.sidebar.radio("Select View Section", [
        "ESG Data", 
        "Shariah DataFeed Data", 
        "Aggregated Reports"
    ])
    
    if view_section == "ESG Data":
        render_esg_data_view()
    elif view_section == "Shariah DataFeed Data":
        render_shariah_data_view()
    elif view_section == "Aggregated Reports":
        st.subheader("Aggregated Data Reports")
        
        report_section = st.radio("Select report type", [
            "ESG Aggregated Data", 
            "Shariah DataFeed Aggregated Data"
        ])
        
        if report_section == "ESG Aggregated Data":
            render_esg_aggregated_view()
        elif report_section == "Shariah DataFeed Aggregated Data":
            render_shariah_aggregated_view() 