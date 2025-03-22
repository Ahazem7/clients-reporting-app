import streamlit as st
import pandas as pd
from typing import Dict, Any, List, Optional, Callable
import logging


def create_page_header(title: str, subtitle: Optional[str] = None):
    """Create a page header with optional subtitle
    
    Args:
        title: Page title
        subtitle: Optional subtitle
    """
    st.title(title)
    if subtitle:
        st.markdown(f"*{subtitle}*")
    st.markdown("---")
    
def show_data_table(data: pd.DataFrame, selection: bool = False, pagination: bool = True, 
                  page_size: int = 10, key: Optional[str] = None):
    """Show a data table with options for selection and pagination
    
    Args:
        data: DataFrame to display
        selection: Whether to allow row selection
        pagination: Whether to paginate the data
        page_size: Number of rows per page
        key: Optional key for the table
    
    Returns:
        selected_indices: Selected row indices if selection is True
    """
    if data.empty:
        st.info("No data available")
        return None
        
    # Handle pagination
    if pagination and len(data) > page_size:
        table_key = f"{key}_pagination" if key else "pagination"
        page_num = st.session_state.get(f"{table_key}_page", 0)
        total_pages = (len(data) - 1) // page_size + 1
        
        col1, col2, col3 = st.columns([1, 3, 1])
        
        with col1:
            if st.button("< Previous", key=f"{table_key}_prev", disabled=(page_num == 0)):
                st.session_state[f"{table_key}_page"] = max(0, page_num - 1)
                st.experimental_rerun()
                
        with col2:
            st.markdown(f"<div style='text-align: center'>Page {page_num + 1} of {total_pages}</div>", unsafe_allow_html=True)
            
        with col3:
            if st.button("Next >", key=f"{table_key}_next", disabled=(page_num >= total_pages - 1)):
                st.session_state[f"{table_key}_page"] = min(total_pages - 1, page_num + 1)
                st.experimental_rerun()
                
        # Slice data for current page
        start_idx = page_num * page_size
        end_idx = start_idx + page_size
        paged_data = data.iloc[start_idx:end_idx].copy()
    else:
        paged_data = data.copy()
        
    # Display table with selection if needed
    table_key = f"{key}_table" if key else "table"
    if selection:
        # Add a "Select" button column for each row to make selection more explicit
        if "select_button" not in st.session_state:
            st.session_state["select_button"] = {}
        
        # Create a clickable table with proper sizing
        col1, col2 = st.columns([1, 5])
        
        with col1:
            for i, _ in enumerate(paged_data.index):
                row_id = paged_data.iloc[i].get('id', i)
                button_key = f"select_row_{key}_{row_id}"
                
                if st.button(f"Select", key=button_key):
                    selection_key = f"{key}_selection"
                    st.session_state[selection_key] = i
                    return i  # Return the selected index
        
        with col2:
            st.dataframe(paged_data, use_container_width=True, hide_index=True)
        
        # Check if we have a stored selection
        selection_key = f"{key}_selection"
        if selection_key in st.session_state:
            return st.session_state[selection_key]
        
        return None
    else:
        st.dataframe(paged_data, use_container_width=True, hide_index=True)
        return None

def show_editable_data_table(data: pd.DataFrame, 
                          on_change: Callable[[pd.DataFrame], None], 
                          editor_height: int = 500, 
                          column_config: Optional[Dict] = None,
                          key: Optional[str] = None):
    """Show an editable data table and handle changes
    
    Args:
        data: DataFrame to display
        on_change: Callback function when data is edited
        editor_height: Height of the editor in pixels
        column_config: Optional column configuration for the data editor
        key: Optional key for the table
    """
    if data.empty:
        st.info("No data available to edit")
        return
    
    # Clone the data to avoid modifying the original
    df_to_edit = data.copy()
    
    # Create a unique key for this editor
    editor_key = f"data_editor_{key}" if key else "data_editor"
    
    # Set up default column configuration if not provided
    if column_config is None:
        # Make ID column non-editable
        column_config = {
            "id": st.column_config.Column(
                "ID", 
                disabled=True,
                width="small"
            )
        }
    
    try:
        # Show the editable data table with the specified configuration
        edited_df = st.data_editor(
            df_to_edit, 
            use_container_width=True,
            num_rows="fixed",
            height=editor_height,
            column_config=column_config,
            key=editor_key,
            hide_index=True
        )
        
        # Check if data was changed
        if not edited_df.equals(df_to_edit):
            # Call the on_change callback with the edited data
            on_change(edited_df)
    except Exception as e:
        st.error(f"Error in data editor: {str(e)}")
        logging.error(f"Data editor error: {str(e)}", exc_info=True)

def show_filter_sidebar(data: pd.DataFrame, columns: List[str], key_prefix: str = "filter"):
    """Show filters in the sidebar for the given columns
    
    Args:
        data: DataFrame containing the data
        columns: List of column names to filter on
        key_prefix: Prefix for filter keys
        
    Returns:
        DataFrame: Filtered data
    """
    st.sidebar.markdown("## Filters")
    
    filtered_data = data.copy()
    has_filters_applied = False
    
    for col in columns:
        if col in data.columns:
            unique_values = sorted(data[col].dropna().unique())
            
            if len(unique_values) > 1:
                filter_key = f"{key_prefix}_{col}"
                
                if len(unique_values) <= 10:
                    # For columns with few unique values, use multiselect
                    selected_values = st.sidebar.multiselect(
                        f"Filter by {col}",
                        options=unique_values,
                        default=[],
                        key=filter_key
                    )
                    
                    if selected_values:
                        has_filters_applied = True
                        filtered_data = filtered_data[filtered_data[col].isin(selected_values)]
                else:
                    # For columns with many unique values, use text input
                    filter_value = st.sidebar.text_input(
                        f"Filter by {col}",
                        "",
                        key=filter_key
                    )
                    
                    if filter_value:
                        has_filters_applied = True
                        filtered_data = filtered_data[filtered_data[col].astype(str).str.contains(filter_value, case=False)]
    
    # Add a button to clear all filters
    if has_filters_applied and st.sidebar.button("Clear All Filters", key=f"{key_prefix}_clear_all"):
        # Reset all filter widgets by clearing session state
        for key in list(st.session_state.keys()):
            if key.startswith(f"{key_prefix}_"):
                del st.session_state[key]
        st.experimental_rerun()
                        
    return filtered_data
    
def show_error_message(message: str):
    """Show an error message
    
    Args:
        message: Error message
    """
    st.error(message)
    
def show_success_message(message: str):
    """Show a success message
    
    Args:
        message: Success message
    """
    st.success(message)
    
def show_loading_spinner(message: str, func: Callable, **kwargs):
    """Show a loading spinner while executing a function
    
    Args:
        message: Message to display during loading
        func: Function to execute
        **kwargs: Arguments to pass to the function
        
    Returns:
        Any: Result of the function
    """
    with st.spinner(message):
        return func(**kwargs)
        
def confirm_action(message: str, key: str) -> bool:
    """Show a confirmation dialog
    
    Args:
        message: Confirmation message
        key: Unique key for the confirmation dialog
        
    Returns:
        bool: True if confirmed, False otherwise
    """
    # Check if key already exists in session state, initialize if not
    if key not in st.session_state:
        st.session_state[key] = False
    
    confirm = st.checkbox(message, key=key)
    
    # When user unselects, reset the state
    if not confirm and st.session_state[key]:
        st.session_state[key] = False
    
    return confirm
    
def format_comma_separated_list(text: str) -> str:
    """Format a comma-separated list for display
    
    Args:
        text: Comma-separated text
        
    Returns:
        str: Formatted HTML for the list
    """
    if not text or pd.isna(text):
        return ""
        
    items = [item.strip() for item in text.split(',') if item.strip()]
    if not items:
        return ""
        
    return ", ".join(items) 