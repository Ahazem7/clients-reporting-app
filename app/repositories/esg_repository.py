import sqlite3
import pandas as pd
import logging
from typing import List, Dict, Any, Optional, Tuple
from app.config import Config

logger = logging.getLogger(__name__)

class ESGRepository:
    """Repository for ESG data operations"""
    
    def __init__(self, db_path: Optional[str] = None):
        """Initialize the ESG repository
        
        Args:
            db_path: Optional database path (default: from config)
        """
        self.db_path = db_path or Config.DATABASE_PATH
        self.table_name = Config.DB.ESG_TABLE
        
    def _get_connection(self) -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
        """Get a database connection and cursor
        
        Returns:
            Tuple[sqlite3.Connection, sqlite3.Cursor]: Connection and cursor
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            return conn, cursor
        except sqlite3.Error as e:
            logger.error(f"Error connecting to database: {e}")
            raise
    
    def get_all(self) -> pd.DataFrame:
        """Get all ESG data
        
        Returns:
            pd.DataFrame: ESG data
        """
        try:
            conn, cursor = self._get_connection()
            cursor.execute(f"SELECT * FROM {self.table_name}")
            rows = cursor.fetchall()
            return pd.DataFrame([dict(row) for row in rows])
        except sqlite3.Error as e:
            logger.error(f"Error getting all ESG data: {e}")
            return pd.DataFrame()
        finally:
            if conn:
                conn.close()
                
    def get_by_id(self, record_id: int) -> pd.DataFrame:
        """Get ESG data by ID
        
        Args:
            record_id: Record ID
            
        Returns:
            pd.DataFrame: ESG data
        """
        try:
            conn, cursor = self._get_connection()
            cursor.execute(f"SELECT * FROM {self.table_name} WHERE id = ?", (record_id,))
            rows = cursor.fetchall()
            return pd.DataFrame([dict(row) for row in rows])
        except sqlite3.Error as e:
            logger.error(f"Error getting ESG data by ID {record_id}: {e}")
            return pd.DataFrame()
        finally:
            if conn:
                conn.close()
                
    def get_by_client(self, client: str) -> pd.DataFrame:
        """Get ESG data by client
        
        Args:
            client: Client name
            
        Returns:
            pd.DataFrame: ESG data
        """
        try:
            conn, cursor = self._get_connection()
            cursor.execute(f"SELECT * FROM {self.table_name} WHERE client = ?", (client,))
            rows = cursor.fetchall()
            return pd.DataFrame([dict(row) for row in rows])
        except sqlite3.Error as e:
            logger.error(f"Error getting ESG data for client {client}: {e}")
            return pd.DataFrame()
        finally:
            if conn:
                conn.close()
                
    def add(self, data: Dict[str, Any]) -> int:
        """Add a new ESG data record
        
        Args:
            data: ESG data
            
        Returns:
            int: New record ID
        """
        try:
            conn, cursor = self._get_connection()
            
            # Extract column names and values
            columns = list(data.keys())
            placeholders = ', '.join(['?'] * len(columns))
            values = [data[col] for col in columns]
            
            # Build and execute query
            query = f"INSERT INTO {self.table_name} ({', '.join(columns)}) VALUES ({placeholders})"
            cursor.execute(query, values)
            conn.commit()
            
            return cursor.lastrowid
        except sqlite3.Error as e:
            logger.error(f"Error adding ESG data: {e}")
            raise
        finally:
            if conn:
                conn.close()
                
    def update(self, record_id: int, data: Dict[str, Any]) -> bool:
        """Update an ESG data record
        
        Args:
            record_id: Record ID
            data: Updated ESG data
            
        Returns:
            bool: True if successful
        """
        try:
            conn, cursor = self._get_connection()
            
            # Extract column names and values, excluding ID
            update_data = {k: v for k, v in data.items() if k != 'id'}
            set_clause = ', '.join([f"{col} = ?" for col in update_data.keys()])
            values = list(update_data.values()) + [record_id]
            
            # Build and execute query
            query = f"UPDATE {self.table_name} SET {set_clause} WHERE id = ?"
            cursor.execute(query, values)
            conn.commit()
            
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            logger.error(f"Error updating ESG data with ID {record_id}: {e}")
            raise
        finally:
            if conn:
                conn.close()
                
    def delete(self, record_id: int) -> bool:
        """Delete an ESG data record
        
        Args:
            record_id: Record ID
            
        Returns:
            bool: True if successful
        """
        try:
            conn, cursor = self._get_connection()
            cursor.execute(f"DELETE FROM {self.table_name} WHERE id = ?", (record_id,))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            logger.error(f"Error deleting ESG data with ID {record_id}: {e}")
            raise
        finally:
            if conn:
                conn.close()
                
    def search_by_field_value(self, field_name: str, search_term: str) -> pd.DataFrame:
        """Search for ESG data by field value
        
        Args:
            field_name: Field name
            search_term: Search term
            
        Returns:
            pd.DataFrame: Matching ESG data
        """
        try:
            conn, cursor = self._get_connection()
            cursor.execute(f"SELECT * FROM {self.table_name} WHERE {field_name} LIKE ?", (f"%{search_term}%",))
            rows = cursor.fetchall()
            return pd.DataFrame([dict(row) for row in rows])
        except sqlite3.Error as e:
            logger.error(f"Error searching ESG data in field {field_name} for term {search_term}: {e}")
            return pd.DataFrame()
        finally:
            if conn:
                conn.close()
                
    def get_unique_clients(self) -> List[str]:
        """Get a list of unique client names
        
        Returns:
            List[str]: Unique client names
        """
        try:
            conn, cursor = self._get_connection()
            cursor.execute(f"SELECT DISTINCT client FROM {self.table_name} ORDER BY client")
            rows = cursor.fetchall()
            return [row['client'] for row in rows]
        except sqlite3.Error as e:
            logger.error(f"Error getting unique ESG clients: {e}")
            return []
        finally:
            if conn:
                conn.close()
                
    def get_compliance_summary(self) -> Dict[str, int]:
        """Get a summary of compliance status
        
        Returns:
            Dict[str, int]: Counts by compliance status
        """
        try:
            conn, cursor = self._get_connection()
            cursor.execute(f"SELECT compliance, COUNT(*) as count FROM {self.table_name} GROUP BY compliance")
            rows = cursor.fetchall()
            return {row['compliance'] or 'Unknown': row['count'] for row in rows}
        except sqlite3.Error as e:
            logger.error(f"Error getting ESG compliance summary: {e}")
            return {}
        finally:
            if conn:
                conn.close()
                
    def get_aggregated_data(self) -> pd.DataFrame:
        """Get aggregated ESG data by client
        
        Returns:
            pd.DataFrame: Aggregated ESG data
        """
        try:
            conn, cursor = self._get_connection()
            query = f"""
                SELECT 
                    client,
                    GROUP_CONCAT(DISTINCT fields) AS fields,
                    GROUP_CONCAT(DISTINCT data_type) AS data_types,
                    GROUP_CONCAT(DISTINCT data_source) AS data_sources,
                    SUM(sedol_count) AS total_sedol_count,
                    SUM(isin_count) AS total_isin_count,
                    SUM(cusip_count) AS total_cusip_count,
                    GROUP_CONCAT(DISTINCT compliance) AS compliance_status,
                    COUNT(*) AS record_count
                FROM {self.table_name}
                GROUP BY client
                ORDER BY client
            """
            cursor.execute(query)
            rows = cursor.fetchall()
            return pd.DataFrame([dict(row) for row in rows])
        except sqlite3.Error as e:
            logger.error(f"Error getting aggregated ESG data: {e}")
            return pd.DataFrame()
        finally:
            if conn:
                conn.close()
                
    def bulk_add(self, data: pd.DataFrame) -> bool:
        """Add multiple ESG data records
        
        Args:
            data: DataFrame with ESG data
            
        Returns:
            bool: True if successful
        """
        if data.empty:
            return False
            
        try:
            conn, cursor = self._get_connection()
            
            # Get column names from the data
            columns = list(data.columns)
            placeholders = ', '.join(['?'] * len(columns))
            
            # Build the query
            query = f"INSERT INTO {self.table_name} ({', '.join(columns)}) VALUES ({placeholders})"
            
            # Execute for each row
            for _, row in data.iterrows():
                values = [row[col] for col in columns]
                cursor.execute(query, values)
                
            conn.commit()
            return True
        except sqlite3.Error as e:
            logger.error(f"Error bulk adding ESG data: {e}")
            if conn:
                conn.rollback()
            raise
        finally:
            if conn:
                conn.close() 