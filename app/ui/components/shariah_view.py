import streamlit as st
import pandas as pd
import traceback
from typing import Optional
from app.services.shariah_service import ShariahService, get_all_shariah_data, update_shariah_data, delete_shariah_data
from app.ui.components.ui_helpers import (
    show_data_table, 
    show_editable_data_table,
    show_filter_sidebar,
    confirm_action,
    show_success_message,
    show_error_message
)
from app.models.shariah_model import ShariahData


def render_shariah_data_view():
    """Render the Shariah data view with filtering and editing capabilities"""
    st.header("Shariah Data View")
    
    # Get all Shariah data
    shariah_data = get_all_shariah_data()
    
    if shariah_data.empty:
        st.info("No Shariah data available. Please add data in the Inputs page.")
        return
    
    # Create tabs for different views
    tab1, tab2 = st.tabs(["View Data", "Edit Data"])
    
    with tab1:
        # Show filters in the sidebar when this tab is active
        filtered_data = shariah_data
        
        # Track the current tab without resetting filters
        if "shariah_tab" not in st.session_state or st.session_state["shariah_tab"] != "view":
            st.session_state["shariah_tab"] = "view"
            # Don't reset filter state when switching to this tab
        
        # Add sidebar filters
        with st.sidebar:
            st.subheader("Filter Shariah Data")
            filter_columns = ["client", "fields", "frequency", "current_source", "universe"]
            filtered_data = show_filter_sidebar(shariah_data, filter_columns, key_prefix="filter_shariah")
        
        # Show the filtered data table
        st.write(f"Showing {len(filtered_data)} records")
        show_data_table(filtered_data, key="shariah_view")
    
    with tab2:
        st.subheader("Edit Shariah Data")
        
        # Reset tab state if needed
        if "shariah_tab" not in st.session_state or st.session_state["shariah_tab"] != "edit":
            st.session_state["shariah_tab"] = "edit"
        
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
                help="Shariah fields"
            ),
            "data_type": st.column_config.SelectboxColumn(
                "Data Type",
                width="medium",
                options=[
                    "Compliance",
                    "Screening",
                    "Purification",
                    "Reports",
                    "Other"
                ],
                help="Type of Shariah data"
            ),
            "data_source": st.column_config.SelectboxColumn(
                "Data Source",
                width="medium",
                options=[
                    "Refinitiv",
                    "IdealRatings",
                    "S&P",
                    "MSCI",
                    "Internal",
                    "Other"
                ],
                help="Source of the Shariah data"
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
            ),
            "frequency": st.column_config.SelectboxColumn(
                "Frequency",
                width="medium",
                options=[
                    "Daily",
                    "Weekly",
                    "Monthly",
                    "Quarterly",
                    "Annually"
                ],
                help="Frequency of data updates"
            )
        }
        
        # Define callback for data updates
        def on_data_change(updated_df):
            success = update_shariah_data(updated_df)
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
                options=shariah_data["id"].tolist(),
                format_func=lambda x: f"ID: {x} - {shariah_data[shariah_data['id'] == x]['client'].values[0]}",
                key="shariah_delete_select"
            )
        
        with col2:
            if st.button("Delete Selected Record", key="shariah_delete_button"):
                if selected_row:
                    if delete_shariah_data(selected_row):
                        st.success(f"Record ID {selected_row} deleted successfully!")
                        st.rerun()
                    else:
                        st.error("Failed to delete record. Please try again.")
                else:
                    st.warning("Please select a record to delete.")
        
        st.divider()
        
        # Show the editable data table with our custom configuration
        show_editable_data_table(
            shariah_data,
            on_change=on_data_change,
            editor_height=500,
            column_config=column_config,
            key="shariah_editor"
        )
        
        st.info("Edit data directly in the table above. Changes are saved automatically when you edit a cell.")


def render_shariah_aggregated_view(service: Optional[ShariahService] = None):
    """Render aggregated Shariah data view
    
    Args:
        service: Optional Shariah service instance
    """
    service = service or ShariahService()
    
    st.subheader("Aggregated Shariah Data")
    
    # Get aggregated Shariah data
    aggregated_data = service.get_aggregated_data()
    
    if not aggregated_data:
        st.info("No Shariah data available for aggregation.")
        return
        
    # Convert to DataFrame for display
    df = pd.DataFrame([d.to_dict() for d in aggregated_data])
    
    # Add filters to sidebar
    filter_columns = ['client', 'universe', 'frequencies', 'sources']
    filtered_df = show_filter_sidebar(df, filter_columns, key_prefix="shariah_agg_view")
    
    # Display data
    show_data_table(filtered_df, key="shariah_aggregated_data")
    
    # Display frequency summary
    st.subheader("Frequency Summary")
    frequency_summary = service.get_frequency_summary()
    
    if frequency_summary:
        summary_df = pd.DataFrame({
            'Frequency': list(frequency_summary.keys()),
            'Count': list(frequency_summary.values())
        })
        st.dataframe(summary_df)
        
        # Show chart if there's data
        if len(frequency_summary) > 0:
            st.bar_chart(summary_df.set_index('Frequency'))
            
    # Universe count by client
    st.subheader("Universe Count by Client")
    
    # The aggregated data should have 'total_universe_count' based on the repository query
    if not df.empty:
        try:
            if 'total_universe_count' in df.columns:
                # Create a copy of the dataframe with just the columns we need
                universe_df = df[['client', 'total_universe_count']].copy()
                # Replace NaN values with 0
                universe_df['total_universe_count'] = universe_df['total_universe_count'].fillna(0)
                # Convert to int to avoid numerical issues
                universe_df['total_universe_count'] = universe_df['total_universe_count'].astype(int)
                # Sort by universe count
                universe_df = universe_df.sort_values('total_universe_count', ascending=False)
                # Display chart
                st.bar_chart(universe_df.set_index('client'))
            else:
                st.info("Universe count data is not available.")
        except Exception as e:
            st.error("An error occurred while displaying the Universe Count chart.") 