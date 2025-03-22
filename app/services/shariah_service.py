import pandas as pd
import logging
from typing import List, Dict, Any, Optional, Union
import os
from datetime import datetime

from app.database import get_connection
from app.models.shariah_model import ShariahData, ShariahAggregatedData
from app.repositories.shariah_repository import ShariahRepository

logger = logging.getLogger(__name__)

def get_all_shariah_data() -> pd.DataFrame:
    """Get all Shariah data from the database
    
    Returns:
        DataFrame containing all Shariah data records
    """
    try:
        conn = get_connection()
        query = "SELECT * FROM shariah_datafeed"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        logger.error(f"Error retrieving Shariah data: {str(e)}")
        return pd.DataFrame()

def update_shariah_data(updated_df: pd.DataFrame) -> bool:
    """Update Shariah data records in the database
    
    Args:
        updated_df: DataFrame containing updated Shariah records
        
    Returns:
        True if update was successful, False otherwise
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        for _, row in updated_df.iterrows():
            # Ensure numeric fields are properly converted
            sedol_count = int(row.get('sedol_count', 0) or 0)
            isin_count = int(row.get('isin_count', 0) or 0)
            cusip_count = int(row.get('cusip_count', 0) or 0)
            
            query = """
            UPDATE shariah_datafeed 
            SET client = ?, fields = ?, data_type = ?, data_source = ?,
                sedol_count = ?, isin_count = ?, cusip_count = ?, compliance = ?,
                frequency = ?, updated_at = ?
            WHERE id = ?
            """
            
            cursor.execute(query, (
                row.get('client', ''),
                row.get('fields', ''),
                row.get('data_type', ''),
                row.get('data_source', ''),
                sedol_count,
                isin_count,
                cusip_count,
                row.get('compliance', ''),
                row.get('frequency', ''),
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                int(row['id'])
            ))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        logger.error(f"Error updating Shariah data: {str(e)}")
        return False

def delete_shariah_data(record_id: int) -> bool:
    """Delete Shariah data record from the database
    
    Args:
        record_id: ID of the record to delete
        
    Returns:
        True if deletion was successful, False otherwise
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = "DELETE FROM shariah_datafeed WHERE id = ?"
        cursor.execute(query, (record_id,))
        conn.commit()
        
        # Check if any row was affected
        if cursor.rowcount > 0:
            conn.close()
            return True
        else:
            conn.close()
            return False
    except Exception as e:
        logger.error(f"Error deleting Shariah data: {str(e)}")
        return False

class ShariahService:
    """Service class for Shariah data operations"""
    
    def __init__(self):
        """Initialize the Shariah service"""
        self.repository = ShariahRepository()
    
    def add_shariah_data(self, shariah_data: Dict[str, Any]) -> int:
        """Add new Shariah data to the database
        
        Args:
            shariah_data: Dictionary containing Shariah data fields
            
        Returns:
            ID of the newly created record, or -1 if operation failed
        """
        try:
            # Ensure numeric fields are properly converted
            sedol_count = int(shariah_data.get('sedol_count', 0) or 0)
            isin_count = int(shariah_data.get('isin_count', 0) or 0) 
            cusip_count = int(shariah_data.get('cusip_count', 0) or 0)
            
            conn = get_connection()
            cursor = conn.cursor()
            
            # Insert new record
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            query = """
            INSERT INTO shariah_datafeed (
                client, fields, data_type, data_source, 
                sedol_count, isin_count, cusip_count, compliance,
                frequency, created_at, updated_at
            ) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            
            cursor.execute(query, (
                shariah_data.get('client', ''),
                shariah_data.get('fields', ''),
                shariah_data.get('data_type', ''),
                shariah_data.get('data_source', ''),
                sedol_count,
                isin_count,
                cusip_count,
                shariah_data.get('compliance', ''),
                shariah_data.get('frequency', ''),
                now,
                now
            ))
            
            conn.commit()
            record_id = cursor.lastrowid
            conn.close()
            
            return record_id
        except Exception as e:
            logger.error(f"Error adding Shariah data: {str(e)}")
            return -1
    
    def get_shariah_data_by_id(self, record_id: int) -> Optional[Dict[str, Any]]:
        """Get Shariah data by ID
        
        Args:
            record_id: ID of the record to retrieve
            
        Returns:
            Dictionary containing Shariah data or None if not found
        """
        try:
            conn = get_connection()
            query = "SELECT * FROM shariah_datafeed WHERE id = ?"
            df = pd.read_sql(query, conn, params=(record_id,))
            conn.close()
            
            if df.empty:
                return None
            
            return df.iloc[0].to_dict()
        except Exception as e:
            logger.error(f"Error retrieving Shariah data by ID: {str(e)}")
            return None
    
    def import_shariah_data_from_df(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Import Shariah data from a DataFrame
        
        Args:
            df: DataFrame containing Shariah data to import
            
        Returns:
            Dictionary with results of the import operation
        """
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            # Track import results
            records_added = 0
            records_skipped = 0
            errors = []
            
            for _, row in df.iterrows():
                try:
                    # Validate required fields
                    if not row.get('client') or pd.isna(row.get('client')):
                        records_skipped += 1
                        errors.append(f"Row skipped: Missing client name")
                        continue
                    
                    # Ensure numeric fields are properly converted
                    sedol_count = int(row.get('sedol_count', 0) or 0)
                    isin_count = int(row.get('isin_count', 0) or 0)
                    cusip_count = int(row.get('cusip_count', 0) or 0)
                    
                    # Insert new record
                    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    query = """
                    INSERT INTO shariah_datafeed (
                        client, fields, data_type, data_source, 
                        sedol_count, isin_count, cusip_count, compliance,
                        frequency, created_at, updated_at
                    ) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """
                    
                    cursor.execute(query, (
                        row.get('client', ''),
                        row.get('fields', ''),
                        row.get('data_type', ''),
                        row.get('data_source', ''),
                        sedol_count,
                        isin_count,
                        cusip_count,
                        row.get('compliance', ''),
                        row.get('frequency', ''),
                        now,
                        now
                    ))
                    
                    records_added += 1
                except Exception as row_error:
                    records_skipped += 1
                    errors.append(f"Error in row: {str(row_error)}")
            
            conn.commit()
            conn.close()
            
            return {
                "success": True,
                "records_added": records_added,
                "records_skipped": records_skipped,
                "errors": errors
            }
        except Exception as e:
            logger.error(f"Error importing Shariah data: {str(e)}")
            return {
                "success": False,
                "records_added": 0,
                "records_skipped": 0,
                "errors": [str(e)]
            }
    
    def get_shariah_metrics(self) -> Dict[str, Any]:
        """Get metrics for Shariah data in the database
        
        Returns:
            Dictionary containing metrics about Shariah data
        """
        try:
            conn = get_connection()
            
            # Total records
            query_total = "SELECT COUNT(*) as count FROM shariah_datafeed"
            df_total = pd.read_sql(query_total, conn)
            total_records = int(df_total.iloc[0]['count']) if not df_total.empty else 0
            
            # Unique clients
            query_clients = "SELECT COUNT(DISTINCT client) as count FROM shariah_datafeed"
            df_clients = pd.read_sql(query_clients, conn)
            unique_clients = int(df_clients.iloc[0]['count']) if not df_clients.empty else 0
            
            # Compliance breakdown
            query_compliance = "SELECT compliance, COUNT(*) as count FROM shariah_datafeed GROUP BY compliance"
            df_compliance = pd.read_sql(query_compliance, conn)
            
            # Data source breakdown
            query_source = "SELECT data_source, COUNT(*) as count FROM shariah_datafeed GROUP BY data_source"
            df_source = pd.read_sql(query_source, conn)
            
            # Frequency breakdown
            query_frequency = "SELECT frequency, COUNT(*) as count FROM shariah_datafeed GROUP BY frequency"
            df_frequency = pd.read_sql(query_frequency, conn)
            
            conn.close()
            
            # Format results
            compliance_data = {}
            for _, row in df_compliance.iterrows():
                if not pd.isna(row['compliance']) and row['compliance']:
                    compliance_data[row['compliance']] = int(row['count'])
                
            source_data = {}
            for _, row in df_source.iterrows():
                if not pd.isna(row['data_source']) and row['data_source']:
                    source_data[row['data_source']] = int(row['count'])
                    
            frequency_data = {}
            for _, row in df_frequency.iterrows():
                if not pd.isna(row['frequency']) and row['frequency']:
                    frequency_data[row['frequency']] = int(row['count'])
            
            return {
                "total_records": total_records,
                "unique_clients": unique_clients,
                "compliance_breakdown": compliance_data,
                "source_breakdown": source_data,
                "frequency_breakdown": frequency_data
            }
        except Exception as e:
            logger.error(f"Error getting Shariah metrics: {str(e)}")
            return {
                "total_records": 0,
                "unique_clients": 0,
                "compliance_breakdown": {},
                "source_breakdown": {},
                "frequency_breakdown": {}
            }
    
    def get_aggregated_data(self) -> List[ShariahAggregatedData]:
        """Get aggregated Shariah data by client
        
        Returns:
            List of ShariahAggregatedData objects
        """
        try:
            df = self.repository.get_aggregated_data()
            
            if df.empty:
                return []
                
            # Convert DataFrame rows to ShariahAggregatedData objects
            aggregated_data = []
            for _, row in df.iterrows():
                data_dict = row.to_dict()
                aggregated_data.append(ShariahAggregatedData.from_dict(data_dict))
                
            return aggregated_data
        except Exception as e:
            logger.error(f"Error getting aggregated Shariah data: {str(e)}")
            return []
            
    def get_frequency_summary(self) -> Dict[str, int]:
        """Get a summary of frequency counts
        
        Returns:
            Dict[str, int]: Counts by frequency
        """
        try:
            return self.repository.get_frequency_summary()
        except Exception as e:
            logger.error(f"Error getting Shariah frequency summary: {str(e)}")
            return {}
            
    def bulk_import_shariah_data(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Import Shariah data from a DataFrame (bulk upload)
        
        Args:
            df: DataFrame containing Shariah data to import
            
        Returns:
            Dictionary with results of the import operation
        """
        return self.import_shariah_data_from_df(df) 