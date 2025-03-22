import streamlit as st
import pandas as pd
import logging
from app.services.esg_service import ESGService
from app.services.shariah_service import ShariahService
from app.models.esg_model import ESGData
from app.models.shariah_model import ShariahData

logger = logging.getLogger(__name__)

def render_inputs_page():
    """Render the data inputs page"""
    st.title("Data Inputs")
    
    # Initialize services
    esg_service = ESGService()
    shariah_service = ShariahService()
    
    # Create tabs for different data input options
    tab1, tab2, tab3, tab4 = st.tabs([
        "Add ESG Data", 
        "Add Shariah Data", 
        "Upload ESG Master Data", 
        "Upload Shariah Data"
    ])
    
    # Tab 1: Add ESG Data Form
    with tab1:
        st.header("Add New ESG Data")
        st.info("Enter ESG data according to the master template format")
        
        # Form for adding ESG data
        with st.form("esg_form"):
            # Required fields
            client = st.text_input("Client Name*", help="Required")
            fields = st.text_area("Fields*", height=150, help="Required - Enter fields like Carbon footprint, ESG Ratings, etc.")
            
            col1, col2 = st.columns(2)
            with col1:
                data_type = st.text_input("Data Type", placeholder="%, Numeric, Rating, etc.", help="Enter the type of data (e.g., %, Numeric, Rating)")
            with col2:
                data_source = st.text_input("Data Source", placeholder="FactSet, MSCI, etc.", help="Enter the source of the data (e.g., FactSet, MSCI)")
            
            # Count columns
            col3, col4, col5 = st.columns(3)
            with col3:
                sedol_count = st.number_input("SEDOL Count", min_value=0, value=0, help="Number of SEDOL identifiers")
            with col4:
                isin_count = st.number_input("ISIN Count", min_value=0, value=0, help="Number of ISIN identifiers")
            with col5:
                cusip_count = st.number_input("CUSIP Count", min_value=0, value=0, help="Number of CUSIP identifiers")
                
            compliance = st.selectbox(
                "Compliance",
                options=["Yes", "No"],
                index=1,
                help="Is this data compliant with requirements?"
            )
            
            st.markdown("---")
            submitted = st.form_submit_button("Save ESG Data", use_container_width=True)
            
            if submitted:
                if not client or not fields:
                    st.error("Client Name and Fields are required")
                else:
                    try:
                        # Create ESG data object
                        esg_data = {
                            'client': client,
                            'fields': fields,
                            'data_type': data_type if data_type else '',
                            'data_source': data_source if data_source else '',
                            'sedol_count': sedol_count,
                            'isin_count': isin_count,
                            'cusip_count': cusip_count,
                            'compliance': compliance
                        }
                        
                        # Save to database
                        record_id = esg_service.add_esg_data(esg_data)
                        
                        if record_id > 0:
                            st.success(f"ESG data saved successfully with ID: {record_id}")
                            # Clear form with empty placeholder
                            st.experimental_rerun()
                        else:
                            st.error("Error saving ESG data. Please check the logs for details.")
                    except Exception as e:
                        st.error(f"Error saving ESG data: {str(e)}")
                        logger.exception("Error saving ESG data")
    
    # Tab 2: Add Shariah Data Form
    with tab2:
        st.header("Add New Shariah DataFeed Data")
        st.info("Enter Shariah data for client reporting")
        
        # Form for adding Shariah data
        with st.form("shariah_form"):
            # Required fields
            client = st.text_input("Client Name*", help="Required")
            
            col1, col2 = st.columns(2)
            with col1:
                current_source = st.text_input("Current Source", help="Current data source")
                delivery_name = st.text_input("Delivery Name", help="Name of the delivery")
                universe = st.text_input("Universe", help="Universe coverage")
            with col2:
                after_migration = st.text_input("After Migration", help="Source after migration")
                fields = st.text_area("Fields", height=100, help="Comma separated list of fields")
                
            # Counts and details
            col3, col4, col5 = st.columns(3)
            with col3:
                universe_count = st.number_input("Universe Count", min_value=0, value=0, help="Number of securities in universe")
                sedol_count = st.number_input("SEDOL Count", min_value=0, value=0, help="Number of SEDOL identifiers")
            with col4:
                frequency = st.selectbox(
                    "Frequency",
                    options=["Daily", "Weekly", "Monthly", "Quarterly"],
                    index=0,
                    help="Frequency of data delivery"
                )
                isin_count = st.number_input("ISIN Count", min_value=0, value=0, help="Number of ISIN identifiers")
            with col5:
                migration_plan = st.text_input("Migration Plan", help="Plan for migration")
                cusip_count = st.number_input("CUSIP Count", min_value=0, value=0, help="Number of CUSIP identifiers")
                
            st.markdown("---")
            submitted = st.form_submit_button("Save Shariah Data", use_container_width=True)
            
            if submitted:
                if not client:
                    st.error("Client Name is required")
                else:
                    try:
                        # Create Shariah data object
                        shariah_data = {
                            'client': client,
                            'current_source': current_source if current_source else None,
                            'after_migration': after_migration if after_migration else None,
                            'delivery_name': delivery_name if delivery_name else None,
                            'fields': fields if fields else None,
                            'universe': universe if universe else None,
                            'universe_count': universe_count,
                            'frequency': frequency,
                            'migration_plan': migration_plan if migration_plan else None,
                            'sedol_count': sedol_count,
                            'isin_count': isin_count,
                            'cusip_count': cusip_count
                        }
                        
                        # Save to database
                        record_id = shariah_service.add_shariah_data(shariah_data)
                        
                        if record_id > 0:
                            st.success(f"Shariah data saved successfully with ID: {record_id}")
                            # Clear form with empty placeholder
                            st.experimental_rerun()
                        else:
                            st.error("Error saving Shariah data. Please check the logs for details.")
                    except Exception as e:
                        st.error(f"Error saving Shariah data: {str(e)}")
                        logger.exception("Error saving Shariah data")
    
    # Tab 3: Upload ESG Master Data
    with tab3:
        st.header("Upload ESG Master Data")
        st.info("Upload your ESG master data Excel file")
        
        # Template download
        st.subheader("Download Template")
        template_data = {
            "Client": ["Client1", "Client2"],
            "Fields": ["Carbon footprint, ESG Ratings", "Controversies, Carbon metrics"],
            "Data Type": ["%, Numeric, Rating", "Numeric, Text"],
            "Data Source": ["FactSet", "MSCI"],
            "SEDOL Count": [10000, 20000],
            "ISIN Count": [5000, 8000],
            "CUSIP Count": [3000, 4000],
            "Compliance": ["Yes", "No"]
        }
        template_df = pd.DataFrame(template_data)
        
        csv = template_df.to_csv(index=False)
        st.download_button(
            label="Download ESG CSV Template",
            data=csv,
            file_name="esg_template.csv",
            mime="text/csv"
        )
        
        # Example explanation
        with st.expander("See example data explanation"):
            st.markdown("""
            ### ESG Data Fields Explanation
            
            - **Client**: The name of the client (e.g., Company name)
            - **Fields**: List of ESG fields/metrics provided (e.g., Carbon footprint, ESG Ratings, etc.)
            - **Data Type**: Format of the data (e.g., %, Numeric, Rating, Text)
            - **Data Source**: Where the data is sourced from (e.g., FactSet, MSCI, Bloomberg)
            - **SEDOL Count**: Number of securities with SEDOL identifiers
            - **ISIN Count**: Number of securities with ISIN identifiers
            - **CUSIP Count**: Number of securities with CUSIP identifiers
            - **Compliance**: Whether the data is compliant (Yes/No)
            """)
        
        # File upload
        st.subheader("Upload ESG Master Data")
        uploaded_file = st.file_uploader("Choose Excel or CSV file", type=["xlsx", "csv"], key="esg_upload")
        
        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
                
                # Rename columns to match database names if needed
                column_mapping = {
                    'Client': 'client',
                    'Fields': 'fields',
                    'Data Type': 'data_type',
                    'Data Source': 'data_source',
                    'SEDOL Count': 'sedol_count',
                    'ISIN Count': 'isin_count',
                    'CUSIP Count': 'cusip_count',
                    'Compliance': 'compliance'
                }
                
                # Create a copy to avoid modifying the view
                df_display = df.copy()
                
                # Show the data
                st.dataframe(df_display)
                
                if st.button("Import ESG Data", type="primary"):
                    # Check required columns
                    expected_columns = ["Client", "Fields"]
                    missing_columns = [col for col in expected_columns if col not in df.columns]
                    
                    if missing_columns:
                        st.error(f"Missing required columns: {', '.join(missing_columns)}")
                    else:
                        # Rename columns for database compatibility
                        df_upload = df.copy()
                        for old_col, new_col in column_mapping.items():
                            if old_col in df_upload.columns:
                                df_upload.rename(columns={old_col: new_col}, inplace=True)
                        
                        # Import data
                        result = esg_service.bulk_import_esg_data(df_upload)
                        if result:
                            st.success(f"Successfully imported {len(df)} ESG data records")
                        else:
                            st.error("Failed to import ESG data")
            except Exception as e:
                st.error(f"Error processing file: {str(e)}")
                logger.exception("Error processing ESG file")
    
    # Tab 4: Upload Shariah Data
    with tab4:
        st.header("Upload Shariah Data")
        st.info("Upload your Shariah DataFeed data file")
        
        # Template download
        st.subheader("Download Template")
        template_data = {
            "client": ["Client1", "Client2"],
            "current_source": ["SourceA", "SourceB"],
            "after_migration": ["SourceC", "SourceD"],
            "delivery_name": ["Delivery1", "Delivery2"],
            "fields": ["Field1, Field2", "Field3, Field4"],
            "universe": ["Universe1", "Universe2"],
            "universe_count": [1000, 2000],
            "frequency": ["Daily", "Weekly"],
            "migration_plan": ["Plan1", "Plan2"],
            "sedol_count": [300, 400],
            "isin_count": [350, 450],
            "cusip_count": [100, 150]
        }
        template_df = pd.DataFrame(template_data)
        
        csv = template_df.to_csv(index=False)
        st.download_button(
            label="Download Shariah Data Template",
            data=csv,
            file_name="shariah_template.csv",
            mime="text/csv"
        )
        
        # File upload
        st.subheader("Upload Shariah Data")
        uploaded_file = st.file_uploader("Choose CSV or Excel file", type=["csv", "xlsx"], key="shariah_upload")
        
        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
                    
                st.dataframe(df)
                
                if st.button("Import Shariah Data", type="primary"):
                    if "client" not in df.columns:
                        st.error("CSV must include 'client' column")
                    else:
                        result = shariah_service.bulk_import_shariah_data(df)
                        if result:
                            st.success(f"Successfully imported {len(df)} Shariah data records")
                        else:
                            st.error("Failed to import Shariah data")
            except Exception as e:
                st.error(f"Error processing file: {str(e)}")
                logger.exception("Error processing Shariah file") 