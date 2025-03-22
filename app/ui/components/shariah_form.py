import streamlit as st
import pandas as pd
from typing import Dict, Any, Optional
from app.models.shariah_model import ShariahData
from app.services.shariah_service import ShariahService
from app.ui.components.ui_helpers import show_error_message, show_success_message


def render_shariah_form(service: Optional[ShariahService] = None):
    """Render Shariah data input form
    
    Args:
        service: Optional Shariah service instance
    """
    service = service or ShariahService()
    
    st.subheader("Add New Shariah DataFeed Data")
    
    with st.form("shariah_form"):
        client = st.text_input("Client Name")
        current_source = st.text_input("Current Source")
        after_migration = st.text_input("After Migration")
        delivery_name = st.text_input("Delivery Name")
        fields = st.text_area("Fields (separate by commas)")
        universe = st.text_input("Universe")
        universe_count = st.number_input("Universe Count", min_value=0, step=1)
        frequency = st.text_input("Frequency")
        migration_plan = st.text_input("Migration Plan")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            sedol_count = st.number_input("SEDOL Count", min_value=0, step=1)
        with col2:
            isin_count = st.number_input("ISIN Count", min_value=0, step=1)
        with col3:
            cusip_count = st.number_input("CUSIP Count", min_value=0, step=1)
        
        submitted = st.form_submit_button("Submit")
        
        if submitted:
            if not client:
                show_error_message("Please fill out the required field: Client.")
            else:
                try:
                    # Create Shariah data model
                    shariah_data = ShariahData(
                        client=client,
                        current_source=current_source,
                        after_migration=after_migration,
                        delivery_name=delivery_name,
                        fields=fields,
                        universe=universe,
                        universe_count=universe_count,
                        frequency=frequency,
                        migration_plan=migration_plan,
                        sedol_count=sedol_count,
                        isin_count=isin_count,
                        cusip_count=cusip_count
                    )
                    
                    # Add to database
                    record_id = service.add_shariah_data(shariah_data)
                    
                    if record_id:
                        show_success_message("Shariah data added successfully!")
                    else:
                        show_error_message("Failed to add Shariah data.")
                except Exception as e:
                    show_error_message(f"Error adding Shariah data: {str(e)}")
                    
                    
def render_shariah_bulk_upload(service: Optional[ShariahService] = None):
    """Render Shariah data bulk upload form
    
    Args:
        service: Optional Shariah service instance
    """
    service = service or ShariahService()
    
    st.subheader("Bulk Upload Shariah Data")
    
    uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])
    
    if uploaded_file:
        try:
            data = pd.read_excel(uploaded_file)
            
            with st.form("shariah_upload_form"):
                st.write("Click Import to upload the data")
                import_button = st.form_submit_button("Import Data")
                
                if import_button:
                    with st.spinner("Importing data..."):
                        result = service.bulk_import_shariah_data(data)
                        
                        if result:
                            show_success_message(f"Successfully imported {len(data)} records.")
                        else:
                            show_error_message("Failed to import data.")
        except Exception as e:
            show_error_message(f"Error reading file: {str(e)}")
            
            
def render_shariah_edit_form(record_id: int, service: Optional[ShariahService] = None):
    """Render Shariah data edit form
    
    Args:
        record_id: Record ID to edit
        service: Optional Shariah service instance
    """
    service = service or ShariahService()
    
    # Get existing record
    shariah_data = service.get_shariah_data_by_id(record_id)
    
    if not shariah_data:
        show_error_message(f"Record with ID {record_id} not found.")
        return
        
    st.subheader(f"Edit Shariah Data - {shariah_data.client}")
    
    with st.form("shariah_edit_form"):
        client = st.text_input("Client Name", value=shariah_data.client)
        current_source = st.text_input("Current Source", value=shariah_data.current_source or "")
        after_migration = st.text_input("After Migration", value=shariah_data.after_migration or "")
        delivery_name = st.text_input("Delivery Name", value=shariah_data.delivery_name or "")
        fields = st.text_area("Fields (separate by commas)", value=shariah_data.fields or "")
        universe = st.text_input("Universe", value=shariah_data.universe or "")
        universe_count = st.number_input("Universe Count", min_value=0, step=1, value=shariah_data.universe_count)
        frequency = st.text_input("Frequency", value=shariah_data.frequency or "")
        migration_plan = st.text_input("Migration Plan", value=shariah_data.migration_plan or "")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            sedol_count = st.number_input("SEDOL Count", min_value=0, step=1, value=shariah_data.sedol_count)
        with col2:
            isin_count = st.number_input("ISIN Count", min_value=0, step=1, value=shariah_data.isin_count)
        with col3:
            cusip_count = st.number_input("CUSIP Count", min_value=0, step=1, value=shariah_data.cusip_count)
        
        submitted = st.form_submit_button("Update")
        
        if submitted:
            if not client:
                show_error_message("Please fill out the required field: Client.")
            else:
                try:
                    # Create updated Shariah data model
                    updated_shariah_data = ShariahData(
                        client=client,
                        current_source=current_source,
                        after_migration=after_migration,
                        delivery_name=delivery_name,
                        fields=fields,
                        universe=universe,
                        universe_count=universe_count,
                        frequency=frequency,
                        migration_plan=migration_plan,
                        sedol_count=sedol_count,
                        isin_count=isin_count,
                        cusip_count=cusip_count
                    )
                    
                    # Update in database
                    result = service.update_shariah_data(record_id, updated_shariah_data)
                    
                    if result:
                        show_success_message("Shariah data updated successfully!")
                    else:
                        show_error_message("Failed to update Shariah data.")
                except Exception as e:
                    show_error_message(f"Error updating Shariah data: {str(e)}") 