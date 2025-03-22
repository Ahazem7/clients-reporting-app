import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from app.services.esg_service import ESGService, get_all_esg_data
from app.services.shariah_service import ShariahService, get_all_shariah_data
from app.ui.components.ui_helpers import create_page_header


def render_dashboard_page():
    """Render the dashboard page with analytics and visualizations"""
    create_page_header("Dashboard", "Analytics and visualizations")
    
    # Initialize services for metrics and aggregated data
    esg_service = ESGService()
    shariah_service = ShariahService()
    
    # Load data directly as DataFrames
    esg_df = get_all_esg_data()
    shariah_df = get_all_shariah_data()
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="ESG Records", 
            value=len(esg_df) if not esg_df.empty else 0
        )
    
    with col2:
        st.metric(
            label="Shariah Records", 
            value=len(shariah_df) if not shariah_df.empty else 0
        )
    
    with col3:
        unique_esg_clients = esg_df['client'].nunique() if not esg_df.empty and 'client' in esg_df.columns else 0
        st.metric(
            label="ESG Clients", 
            value=unique_esg_clients
        )
    
    with col4:
        unique_shariah_clients = shariah_df['client'].nunique() if not shariah_df.empty and 'client' in shariah_df.columns else 0
        st.metric(
            label="Shariah Clients", 
            value=unique_shariah_clients
        )
    
    # Create visualization tabs
    tab1, tab2 = st.tabs(["ESG Analytics", "Shariah Analytics"])
    
    # Tab 1: ESG Analytics
    with tab1:
        if esg_df.empty:
            st.info("No ESG data available. Please add data in the 'Input Data' section.")
        else:
            st.subheader("ESG Data Analytics")
            
            # Compliance distribution
            if 'compliance' in esg_df.columns:
                compliance_counts = esg_df['compliance'].value_counts().reset_index()
                compliance_counts.columns = ['Compliance', 'Count']
                
                if not compliance_counts.empty:
                    fig_compliance = px.pie(
                        compliance_counts, 
                        values='Count', 
                        names='Compliance',
                        title='ESG Compliance Distribution',
                        color_discrete_sequence=px.colors.qualitative.Safe
                    )
                    st.plotly_chart(fig_compliance, use_container_width=True)
            
            # Client distribution
            col1, col2 = st.columns(2)
            
            with col1:
                # Client counts
                if 'client' in esg_df.columns:
                    client_counts = esg_df["client"].value_counts().reset_index()
                    client_counts.columns = ['Client', 'Count']
                    
                    fig_clients = px.bar(
                        client_counts.head(10), 
                        x='Client', 
                        y='Count',
                        title='Top Clients by ESG Records',
                        color='Count',
                        color_continuous_scale='Viridis'
                    )
                    st.plotly_chart(fig_clients, use_container_width=True)
            
            with col2:
                # Data source distribution
                if 'data_source' in esg_df.columns:
                    source_counts = esg_df['data_source'].value_counts().reset_index()
                    source_counts.columns = ['Data Source', 'Count']
                    
                    fig_sources = px.pie(
                        source_counts, 
                        values='Count', 
                        names='Data Source',
                        title='Data Sources Distribution',
                        hole=0.4
                    )
                    st.plotly_chart(fig_sources, use_container_width=True)
            
            # Identifier counts
            st.subheader("Identifier Coverage")
            
            # Check if all required columns exist
            id_columns = ['sedol_count', 'isin_count', 'cusip_count']
            if all(col in esg_df.columns for col in id_columns):
                identifier_data = {
                    'Type': ['SEDOL', 'ISIN', 'CUSIP'],
                    'Count': [
                        esg_df['sedol_count'].sum(),
                        esg_df['isin_count'].sum(),
                        esg_df['cusip_count'].sum()
                    ]
                }
                identifier_df = pd.DataFrame(identifier_data)
                
                fig_identifiers = px.bar(
                    identifier_df,
                    x='Type',
                    y='Count',
                    title='Identifier Coverage',
                    color='Type',
                    text='Count'
                )
                fig_identifiers.update_traces(texttemplate='%{text:,}', textposition='inside')
                st.plotly_chart(fig_identifiers, use_container_width=True)
            else:
                st.warning("Identifier data is incomplete or missing.")
    
    # Tab 2: Shariah Analytics
    with tab2:
        if shariah_df.empty:
            st.info("No Shariah data available. Please add data in the 'Input Data' section.")
        else:
            st.subheader("Shariah DataFeed Analytics")
            
            # Frequency distribution
            if 'frequency' in shariah_df.columns:
                frequency_counts = shariah_df['frequency'].value_counts().reset_index()
                frequency_counts.columns = ['Frequency', 'Count']
                
                if not frequency_counts.empty:
                    fig_frequency = px.pie(
                        frequency_counts, 
                        values='Count', 
                        names='Frequency',
                        title='Frequency Distribution',
                        color_discrete_sequence=px.colors.qualitative.Pastel
                    )
                    st.plotly_chart(fig_frequency, use_container_width=True)
            
            # Client and universe analysis
            col1, col2 = st.columns(2)
            
            with col1:
                # Client counts
                if 'client' in shariah_df.columns:
                    client_counts = shariah_df["client"].value_counts().reset_index()
                    client_counts.columns = ['Client', 'Count']
                    
                    fig_clients = px.bar(
                        client_counts.head(10), 
                        x='Client', 
                        y='Count',
                        title='Top Clients by Shariah Records',
                        color='Count',
                        color_continuous_scale='Viridis'
                    )
                    st.plotly_chart(fig_clients, use_container_width=True)
            
            with col2:
                # Universe counts by client
                if 'universe_count' in shariah_df.columns and 'client' in shariah_df.columns:
                    universe_by_client = shariah_df.groupby('client')['universe_count'].sum().reset_index()
                    universe_by_client.columns = ['Client', 'Universe Count']
                    universe_by_client = universe_by_client.sort_values('Universe Count', ascending=False).head(10)
                    
                    fig_universe = px.bar(
                        universe_by_client,
                        x='Client',
                        y='Universe Count',
                        title='Top Clients by Universe Size',
                        color='Universe Count',
                        color_continuous_scale='Viridis'
                    )
                    st.plotly_chart(fig_universe, use_container_width=True)
            
            # Migration status
            if 'current_source' in shariah_df.columns and 'after_migration' in shariah_df.columns:
                st.subheader("Migration Analysis")
                
                migration_data = shariah_df[['current_source', 'after_migration']].drop_duplicates()
                
                for _, row in migration_data.iterrows():
                    source = row['current_source'] or 'Unknown'
                    target = row['after_migration'] or 'Unknown'
                    
                    st.write(f"**Migration Path:** {source} → {target}")
                    
                    # Count records for this migration
                    count = shariah_df[
                        (shariah_df['current_source'] == row['current_source']) & 
                        (shariah_df['after_migration'] == row['after_migration'])
                    ].shape[0]
                    
                    st.write(f"Records: {count}")
                    st.markdown("---") 