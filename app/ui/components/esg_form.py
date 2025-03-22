import streamlit as st
import pandas as pd
from typing import Dict, Any, Optional
from app.models.esg_model import ESGData
from app.services.esg_service import ESGService
from app.ui.components.ui_helpers import show_error_message, show_success_message


def render_esg_form(service: Optional[ESGService] = None):
    """Render ESG data input form
    
    Args:
        service: Optional ESG service instance
    """
    service = service or ESGService()
    
    st.subheader("Add New ESG Data")
    
    with st.form("esg_form"):
        client = st.text_input("Client Name")
        fields = st.text_area("Fields (separate by commas)")
        data_type = st.text_input("Data Type (e.g., Numeric, Percentage)")
        data_source = st.text_input("Data Source (e.g., FactSet, Reuters)")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            sedol_count = st.number_input("SEDOL Count", min_value=0, step=1)
        with col2:
            isin_count = st.number_input("ISIN Count", min_value=0, step=1)
        with col3:
            cusip_count = st.number_input("CUSIP Count", min_value=0, step=1)
            
        compliance = st.selectbox("Compliance", ["", "Pass", "Fail", "No", "Partial"])
        
        submitted = st.form_submit_button("Submit")
        
        if submitted:
            if not client or not fields:
                show_error_message("Please fill out all required fields: Client and Fields.")
            else:
                try:
                    # Create ESG data model
                    esg_data = ESGData(
                        client=client,
                        fields=fields,
                        data_type=data_type,
                        data_source=data_source,
                        sedol_count=sedol_count,
                        isin_count=isin_count,
                        cusip_count=cusip_count,
                        compliance=compliance
                    )
                    
                    # Add to database
                    record_id = service.add_esg_data(esg_data)
                    
                    if record_id:
                        show_success_message("ESG data added successfully!")
                    else:
                        show_error_message("Failed to add ESG data.")
                except Exception as e:
                    show_error_message(f"Error adding ESG data: {str(e)}")
                    
                    
def render_esg_bulk_upload(service: Optional[ESGService] = None):
    """Render ESG data bulk upload form
    
    Args:
        service: Optional ESG service instance
    """
    service = service or ESGService()
    
    st.subheader("Bulk Upload ESG Data")
    
    uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])
    
    if uploaded_file:
        try:
            data = pd.read_excel(uploaded_file)
            
            with st.form("esg_upload_form"):
                st.write("Click Import to upload the data")
                import_button = st.form_submit_button("Import Data")
                
                if import_button:
                    with st.spinner("Importing data..."):
                        result = service.bulk_import_esg_data(data)
                        
                        if result:
                            show_success_message(f"Successfully imported {len(data)} records.")
                        else:
                            show_error_message("Failed to import data.")
        except Exception as e:
            show_error_message(f"Error reading file: {str(e)}")
            
            
def render_esg_edit_form(record_id: int, service: Optional[ESGService] = None):
    """Render ESG data edit form
    
    Args:
        record_id: Record ID to edit
        service: Optional ESG service instance
    """
    service = service or ESGService()
    
    # Get existing record
    esg_data = service.get_esg_data_by_id(record_id)
    
    if not esg_data:
        show_error_message(f"Record with ID {record_id} not found.")
        return
        
    st.subheader(f"Edit ESG Data - {esg_data.client}")
    
    with st.form("esg_edit_form"):
        client = st.text_input("Client Name", value=esg_data.client)
        fields = st.text_area("Fields (separate by commas)", value=esg_data.fields)
        data_type = st.text_input("Data Type", value=esg_data.data_type or "")
        data_source = st.text_input("Data Source", value=esg_data.data_source or "")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            sedol_count = st.number_input("SEDOL Count", min_value=0, step=1, value=esg_data.sedol_count)
        with col2:
            isin_count = st.number_input("ISIN Count", min_value=0, step=1, value=esg_data.isin_count)
        with col3:
            cusip_count = st.number_input("CUSIP Count", min_value=0, step=1, value=esg_data.cusip_count)
            
        # Define compliance options and handle "Partial" value
        compliance_options = ["", "Pass", "Fail", "No", "Partial"]
        if esg_data.compliance and esg_data.compliance not in compliance_options:
            compliance_options.append(esg_data.compliance)
            
        # Find the index of the current compliance value
        compliance_index = 0
        if esg_data.compliance:
            try:
                compliance_index = compliance_options.index(esg_data.compliance)
            except ValueError:
                compliance_index = 0
        
        compliance = st.selectbox(
            "Compliance", 
            compliance_options,
            index=compliance_index
        )
        
        submitted = st.form_submit_button("Update")
        
        if submitted:
            if not client or not fields:
                show_error_message("Please fill out all required fields: Client and Fields.")
            else:
                try:
                    # Create updated ESG data model
                    updated_esg_data = ESGData(
                        client=client,
                        fields=fields,
                        data_type=data_type,
                        data_source=data_source,
                        sedol_count=sedol_count,
                        isin_count=isin_count,
                        cusip_count=cusip_count,
                        compliance=compliance
                    )
                    
                    # Update in database
                    result = service.update_esg_data(record_id, updated_esg_data)
                    
                    if result:
                        show_success_message("ESG data updated successfully!")
                    else:
                        show_error_message("Failed to update ESG data.")
                except Exception as e:
                    show_error_message(f"Error updating ESG data: {str(e)}") 