import streamlit as st
import pandas as pd
import traceback
from app.ui.components.esg_form import render_esg_edit_form
from app.ui.components.shariah_form import render_shariah_edit_form
from app.ui.components.ui_helpers import create_page_header, show_data_table
from app.services.esg_service import ESGService
from app.services.shariah_service import ShariahService


def render_edit_page():
    """Render the edit page"""
    create_page_header("Edit Data", "Modify Existing Records")
    
    edit_section = st.sidebar.radio("Select Data Type to Edit", [
        "ESG Data", 
        "Shariah DataFeed Data"
    ])
    
    if edit_section == "ESG Data":
        st.subheader("Edit ESG Data")
        
        try:
            # Get all ESG data
            esg_service = ESGService()
            esg_data = esg_service.get_all_esg_data()
            
            if not esg_data:
                st.warning("No ESG data available to edit.")
                return
            
            # Convert to DataFrame
            df = pd.DataFrame([d.to_dict() for d in esg_data])
            
            # Check if we're in editing mode or selection mode
            if 'esg_edit_mode' not in st.session_state:
                st.session_state['esg_edit_mode'] = False
                st.session_state['esg_selected_id'] = None
            
            # Show selection UI if not in edit mode
            if not st.session_state['esg_edit_mode']:
                st.info("👇 Select a record from the table below, then click 'Edit Selected Record' to make changes.")
                
                # Display data table with selection
                selection = show_data_table(
                    df,
                    selection=True,
                    key="esg_edit_table"
                )
                
                if selection is not None:
                    # If selection has selected rows
                    if isinstance(selection, list) and len(selection) > 0:
                        selected_index = selection[0]
                        
                        if 0 <= selected_index < len(df):
                            # Get the corresponding row from the original DataFrame
                            selected_row = df.iloc[selected_index]
                            
                            if 'id' in selected_row:
                                record_id = int(selected_row['id'])
                                st.success(f"✓ Selected record #{record_id} - {selected_row['client']}")
                                
                                if st.button("Edit Selected Record", key="edit_esg_button"):
                                    st.session_state['esg_edit_mode'] = True
                                    st.session_state['esg_selected_id'] = record_id
                                    st.experimental_rerun()
                    
                    # If selection is a dataframe with edited values
                    elif hasattr(selection, 'index') and len(selection.index) > 0:
                        selected_indices = selection.index.tolist()
                        if selected_indices:
                            # Get first selected row
                            selected_index = selected_indices[0]
                            if 0 <= selected_index < len(df):
                                selected_row = df.iloc[selected_index]
                                
                                if 'id' in selected_row:
                                    record_id = int(selected_row['id'])
                                    st.success(f"✓ Selected record #{record_id} - {selected_row['client']}")
                                    
                                    if st.button("Edit Selected Record", key="edit_esg_button_df"):
                                        st.session_state['esg_edit_mode'] = True
                                        st.session_state['esg_selected_id'] = record_id
                                        st.experimental_rerun()
            
            # Show edit form if in edit mode
            else:
                record_id = st.session_state['esg_selected_id']
                if st.button("← Back to Selection", key="back_to_esg_selection"):
                    st.session_state['esg_edit_mode'] = False
                    st.session_state['esg_selected_id'] = None
                    st.experimental_rerun()
                else:
                    render_esg_edit_form(record_id)
        
        except Exception as e:
            st.error(f"Error processing ESG data: {str(e)}")
            if st.checkbox("Show detailed error information"):
                st.text(traceback.format_exc())
            
    elif edit_section == "Shariah DataFeed Data":
        st.subheader("Edit Shariah DataFeed Data")
        
        try:
            # Get all Shariah data
            shariah_service = ShariahService()
            shariah_data = shariah_service.get_all_shariah_data()
            
            if not shariah_data:
                st.warning("No Shariah data available to edit.")
                return
            
            # Convert to DataFrame
            df = pd.DataFrame([d.to_dict() for d in shariah_data])
            
            # Check if we're in editing mode or selection mode
            if 'shariah_edit_mode' not in st.session_state:
                st.session_state['shariah_edit_mode'] = False
                st.session_state['shariah_selected_id'] = None
            
            # Show selection UI if not in edit mode
            if not st.session_state['shariah_edit_mode']:
                st.info("👇 Select a record from the table below, then click 'Edit Selected Record' to make changes.")
                
                # Display data table with selection
                selection = show_data_table(
                    df,
                    selection=True,
                    key="shariah_edit_table"
                )
                
                if selection is not None:
                    # If selection has selected rows
                    if isinstance(selection, list) and len(selection) > 0:
                        selected_index = selection[0]
                        
                        if 0 <= selected_index < len(df):
                            # Get the corresponding row from the original DataFrame
                            selected_row = df.iloc[selected_index]
                            
                            if 'id' in selected_row:
                                record_id = int(selected_row['id'])
                                st.success(f"✓ Selected record #{record_id} - {selected_row['client']}")
                                
                                if st.button("Edit Selected Record", key="edit_shariah_button"):
                                    st.session_state['shariah_edit_mode'] = True
                                    st.session_state['shariah_selected_id'] = record_id
                                    st.experimental_rerun()
                    
                    # If selection is a dataframe with edited values
                    elif hasattr(selection, 'index') and len(selection.index) > 0:
                        selected_indices = selection.index.tolist()
                        if selected_indices:
                            # Get first selected row
                            selected_index = selected_indices[0]
                            if 0 <= selected_index < len(df):
                                selected_row = df.iloc[selected_index]
                                
                                if 'id' in selected_row:
                                    record_id = int(selected_row['id'])
                                    st.success(f"✓ Selected record #{record_id} - {selected_row['client']}")
                                    
                                    if st.button("Edit Selected Record", key="edit_shariah_button_df"):
                                        st.session_state['shariah_edit_mode'] = True
                                        st.session_state['shariah_selected_id'] = record_id
                                        st.experimental_rerun()
            
            # Show edit form if in edit mode
            else:
                record_id = st.session_state['shariah_selected_id']
                if st.button("← Back to Selection", key="back_to_shariah_selection"):
                    st.session_state['shariah_edit_mode'] = False
                    st.session_state['shariah_selected_id'] = None
                    st.experimental_rerun()
                else:
                    render_shariah_edit_form(record_id)
        
        except Exception as e:
            st.error(f"Error processing Shariah data: {str(e)}")
            if st.checkbox("Show detailed error information"):
                st.text(traceback.format_exc()) 