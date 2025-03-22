import streamlit as st
import pandas as pd
import traceback
from typing import Optional
from app.services.esg_service import ESGService, get_all_esg_data, update_esg_data, delete_esg_data
from app.ui.components.ui_helpers import (
    show_data_table, 
    show_editable_data_table,
    show_filter_sidebar,
    confirm_action,
    show_success_message,
    show_error_message
)
from app.models.esg_model import ESGData


def render_esg_data_view():
    """Render the ESG data view with filtering and editing capabilities"""
    st.header("ESG Data View")
    
    # Get all ESG data
    esg_data = get_all_esg_data()
    
    if esg_data.empty:
        st.info("No ESG data available. Please add data in the Inputs page.")
        return
    
    # Create tabs for different views
    tab1, tab2 = st.tabs(["View Data", "Edit Data"])
    
    with tab1:
        # Show filters in the sidebar when this tab is active
        filtered_data = esg_data
        
        # Track the current tab without resetting filters
        if "esg_tab" not in st.session_state or st.session_state["esg_tab"] != "view":
            st.session_state["esg_tab"] = "view"
            # Don't reset filter state when switching to this tab
        
        # Add sidebar filters
        with st.sidebar:
            st.subheader("Filter ESG Data")
            filter_columns = ["client", "fields", "data_type", "data_source", "compliance"]
            filtered_data = show_filter_sidebar(esg_data, filter_columns, key_prefix="filter_esg")
        
        # Show the filtered data table
        st.write(f"Showing {len(filtered_data)} records")
        show_data_table(filtered_data, key="esg_view")
    
    with tab2:
        st.subheader("Edit ESG Data")
        
        # Reset tab state if needed
        if "esg_tab" not in st.session_state or st.session_state["esg_tab"] != "edit":
            st.session_state["esg_tab"] = "edit"
        
        # Set up column configuration for the editable table
        column_config = {
            "id": st.column_config.Column(
                "ID",
                disabled=True,
                width="small"
            ),
            "client": st.column_config.TextColumn(
                "Client",
                width="medium",
                help="Client name"
            ),
            "fields": st.column_config.TextColumn(
                "Fields",
                width="medium",
                help="ESG fields"
            ),
            "data_type": st.column_config.SelectboxColumn(
                "Data Type",
                width="medium",
                options=[
                    "Ratings",
                    "Scores",
                    "Metrics",
                    "Reports",
                    "Other"
                ],
                help="Type of ESG data"
            ),
            "data_source": st.column_config.SelectboxColumn(
                "Data Source",
                width="medium",
                options=[
                    "MSCI",
                    "Sustainalytics",
                    "Bloomberg",
                    "Refinitiv",
                    "ISS",
                    "Other"
                ],
                help="Source of the ESG data"
            ),
            "sedol_count": st.column_config.NumberColumn(
                "SEDOL Count",
                width="small",
                min_value=0,
                format="%d",
                help="Number of SEDOLs"
            ),
            "isin_count": st.column_config.NumberColumn(
                "ISIN Count",
                width="small",
                min_value=0,
                format="%d",
                help="Number of ISINs"
            ),
            "cusip_count": st.column_config.NumberColumn(
                "CUSIP Count",
                width="small",
                min_value=0,
                format="%d",
                help="Number of CUSIPs"
            ),
            "compliance": st.column_config.SelectboxColumn(
                "Compliance",
                width="medium",
                options=[
                    "Compliant",
                    "Non-Compliant",
                    "Partial",
                    "Unknown"
                ],
                help="Compliance status"
            )
        }
        
        # Define callback for data updates
        def on_data_change(updated_df):
            success = update_esg_data(updated_df)
            if success:
                st.success("Data updated successfully!")
                st.rerun()
            else:
                st.error("Failed to update data. Please try again.")
                
        # Add delete functionality
        col1, col2 = st.columns([3, 1])
        with col1:
            selected_row = st.selectbox(
                "Select record to delete:",
                options=esg_data["id"].tolist(),
                format_func=lambda x: f"ID: {x} - {esg_data[esg_data['id'] == x]['client'].values[0]}",
                key="esg_delete_select"
            )
        
        with col2:
            if st.button("Delete Selected Record", key="esg_delete_button"):
                if selected_row:
                    if delete_esg_data(selected_row):
                        st.success(f"Record ID {selected_row} deleted successfully!")
                        st.rerun()
                    else:
                        st.error("Failed to delete record. Please try again.")
                else:
                    st.warning("Please select a record to delete.")
        
        st.divider()
        
        # Show the editable data table with our custom configuration
        show_editable_data_table(
            esg_data,
            on_change=on_data_change,
            editor_height=500,
            column_config=column_config,
            key="esg_editor"
        )
        
        st.info("Edit data directly in the table above. Changes are saved automatically when you edit a cell.")


def render_esg_aggregated_view(service: Optional[ESGService] = None):
    """Render aggregated ESG data view
    
    Args:
        service: Optional ESG service instance
    """
    service = service or ESGService()
    
    st.subheader("Aggregated ESG Data")
    
    # Get aggregated ESG data
    aggregated_data = service.get_aggregated_data()
    
    if not aggregated_data:
        st.info("No ESG data available for aggregation.")
        return
        
    # Convert to DataFrame for display
    df = pd.DataFrame([d.to_dict() for d in aggregated_data])
    
    # Add filters to sidebar
    filter_columns = ['client', 'data_source']
    filtered_df = show_filter_sidebar(df, filter_columns, key_prefix="esg_agg_view")
    
    # Display data
    show_data_table(filtered_df, key="esg_aggregated_data")
    
    # Display compliance summary
    st.subheader("Compliance Summary")
    compliance_summary = service.get_compliance_summary()
    
    if compliance_summary:
        summary_df = pd.DataFrame({
            'Compliance Status': list(compliance_summary.keys()),
            'Count': list(compliance_summary.values())
        })
        st.dataframe(summary_df)
        
        # Show chart if there's data
        if len(compliance_summary) > 0:
            st.bar_chart(summary_df.set_index('Compliance Status')) 