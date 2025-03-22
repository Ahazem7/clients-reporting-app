import pandas as pd
import logging
from typing import List, Dict, Any, Optional, Union
import os
from datetime import datetime

from app.database import get_connection
from app.models.esg_model import ESGData, ESGAggregatedData
from app.repositories.esg_repository import ESGRepository

logger = logging.getLogger(__name__)

def get_all_esg_data() -> pd.DataFrame:
    """Get all ESG data from the database
    
    Returns:
        DataFrame containing all ESG data records
    """
    try:
        conn = get_connection()
        query = "SELECT * FROM esg_data"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        logger.error(f"Error retrieving ESG data: {str(e)}")
        return pd.DataFrame()

def update_esg_data(updated_df: pd.DataFrame) -> bool:
    """Update ESG data records in the database
    
    Args:
        updated_df: DataFrame containing updated ESG records
        
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
            UPDATE esg_data 
            SET client = ?, fields = ?, data_type = ?, data_source = ?,
                sedol_count = ?, isin_count = ?, cusip_count = ?, compliance = ?,
                updated_at = ?
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
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                int(row['id'])
            ))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        logger.error(f"Error updating ESG data: {str(e)}")
        return False

def delete_esg_data(record_id: int) -> bool:
    """Delete ESG data record from the database
    
    Args:
        record_id: ID of the record to delete
        
    Returns:
        True if deletion was successful, False otherwise
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = "DELETE FROM esg_data WHERE id = ?"
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
        logger.error(f"Error deleting ESG data: {str(e)}")
        return False

class ESGService:
    """Service class for ESG data operations"""
    
    def __init__(self):
        """Initialize the ESG service"""
        self.repository = ESGRepository()
    
    def add_esg_data(self, esg_data: Dict[str, Any]) -> int:
        """Add new ESG data to the database
        
        Args:
            esg_data: Dictionary containing ESG data fields
            
        Returns:
            ID of the newly created record, or -1 if operation failed
        """
        try:
            # Ensure numeric fields are properly converted
            sedol_count = int(esg_data.get('sedol_count', 0) or 0)
            isin_count = int(esg_data.get('isin_count', 0) or 0) 
            cusip_count = int(esg_data.get('cusip_count', 0) or 0)
            
            conn = get_connection()
            cursor = conn.cursor()
            
            # Insert new record
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            query = """
            INSERT INTO esg_data (
                client, fields, data_type, data_source, 
                sedol_count, isin_count, cusip_count, compliance,
                created_at, updated_at
            ) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            
            cursor.execute(query, (
                esg_data.get('client', ''),
                esg_data.get('fields', ''),
                esg_data.get('data_type', ''),
                esg_data.get('data_source', ''),
                sedol_count,
                isin_count,
                cusip_count,
                esg_data.get('compliance', ''),
                now,
                now
            ))
            
            conn.commit()
            record_id = cursor.lastrowid
            conn.close()
            
            # Log successful insertion
            logger.info(f"Successfully added ESG data for client '{esg_data.get('client', '')}' with ID {record_id}")
            
            return record_id
        except Exception as e:
            logger.error(f"Error adding ESG data: {str(e)}")
            return -1
    
    def get_esg_data_by_id(self, record_id: int) -> Optional[Dict[str, Any]]:
        """Get ESG data by ID
        
        Args:
            record_id: ID of the record to retrieve
            
        Returns:
            Dictionary containing ESG data or None if not found
        """
        try:
            conn = get_connection()
            query = "SELECT * FROM esg_data WHERE id = ?"
            df = pd.read_sql(query, conn, params=(record_id,))
            conn.close()
            
            if df.empty:
                return None
            
            return df.iloc[0].to_dict()
        except Exception as e:
            logger.error(f"Error retrieving ESG data by ID: {str(e)}")
            return None
    
    def import_esg_data_from_df(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Import ESG data from a DataFrame
        
        Args:
            df: DataFrame containing ESG data to import
            
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
                    INSERT INTO esg_data (
                        client, fields, data_type, data_source, 
                        sedol_count, isin_count, cusip_count, compliance,
                        created_at, updated_at
                    ) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
            logger.error(f"Error importing ESG data: {str(e)}")
            return {
                "success": False,
                "records_added": 0,
                "records_skipped": 0,
                "errors": [str(e)]
            }
    
    def get_esg_metrics(self) -> Dict[str, Any]:
        """Get metrics for ESG data in the database
        
        Returns:
            Dictionary containing metrics about ESG data
        """
        try:
            conn = get_connection()
            
            # Total records
            query_total = "SELECT COUNT(*) as count FROM esg_data"
            df_total = pd.read_sql(query_total, conn)
            total_records = int(df_total.iloc[0]['count']) if not df_total.empty else 0
            
            # Unique clients
            query_clients = "SELECT COUNT(DISTINCT client) as count FROM esg_data"
            df_clients = pd.read_sql(query_clients, conn)
            unique_clients = int(df_clients.iloc[0]['count']) if not df_clients.empty else 0
            
            # Compliance breakdown
            query_compliance = "SELECT compliance, COUNT(*) as count FROM esg_data GROUP BY compliance"
            df_compliance = pd.read_sql(query_compliance, conn)
            
            # Data source breakdown
            query_source = "SELECT data_source, COUNT(*) as count FROM esg_data GROUP BY data_source"
            df_source = pd.read_sql(query_source, conn)
            
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
            
            return {
                "total_records": total_records,
                "unique_clients": unique_clients,
                "compliance_breakdown": compliance_data,
                "source_breakdown": source_data
            }
        except Exception as e:
            logger.error(f"Error getting ESG metrics: {str(e)}")
            return {
                "total_records": 0,
                "unique_clients": 0,
                "compliance_breakdown": {},
                "source_breakdown": {}
            }
    
    def get_aggregated_data(self) -> List[ESGAggregatedData]:
        """Get aggregated ESG data by client
        
        Returns:
            List of ESGAggregatedData objects
        """
        try:
            df = self.repository.get_aggregated_data()
            
            if df.empty:
                return []
                
            # Convert DataFrame rows to ESGAggregatedData objects
            aggregated_data = []
            for _, row in df.iterrows():
                data_dict = row.to_dict()
                aggregated_data.append(ESGAggregatedData.from_dict(data_dict))
                
            return aggregated_data
        except Exception as e:
            logger.error(f"Error getting aggregated ESG data: {str(e)}")
            return []
            
    def get_compliance_summary(self) -> Dict[str, int]:
        """Get a summary of compliance status
        
        Returns:
            Dict[str, int]: Counts by compliance status
        """
        try:
            return self.repository.get_compliance_summary()
        except Exception as e:
            logger.error(f"Error getting ESG compliance summary: {str(e)}")
            return {}
            
    def bulk_import_esg_data(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Import ESG data from a DataFrame (bulk upload)
        
        Args:
            df: DataFrame containing ESG data to import
            
        Returns:
            Dictionary with results of the import operation
        """
        return self.import_esg_data_from_df(df) 