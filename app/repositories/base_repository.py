import pandas as pd
import logging
from typing import List, Dict, Any, Optional, Tuple, Union
from app.repositories.db_manager import DatabaseManager

logger = logging.getLogger(__name__)

class BaseRepository:
    """Base repository for data access operations"""
    
    def __init__(self, table_name: str, db_manager: Optional[DatabaseManager] = None):
        """Initialize the repository
        
        Args:
            table_name: Name of the database table
            db_manager: Optional database manager instance
        """
        self.table_name = table_name
        self.db_manager = db_manager or DatabaseManager()
        
    def get_all(self) -> pd.DataFrame:
        """Get all records from the table
        
        Returns:
            DataFrame: All records
        """
        with self.db_manager:
            query = f"SELECT * FROM {self.table_name}"
            return self.db_manager.fetch_dataframe(query)
            
    def get_by_id(self, record_id: int) -> pd.DataFrame:
        """Get a record by ID
        
        Args:
            record_id: Record ID
            
        Returns:
            DataFrame: Matching record
        """
        with self.db_manager:
            query = f"SELECT * FROM {self.table_name} WHERE id = ?"
            return self.db_manager.fetch_dataframe(query, (record_id,))
            
    def get_by_field(self, field_name: str, field_value: Any) -> pd.DataFrame:
        """Get records by a field value
        
        Args:
            field_name: Field name
            field_value: Field value
            
        Returns:
            DataFrame: Matching records
        """
        with self.db_manager:
            query = f"SELECT * FROM {self.table_name} WHERE {field_name} = ?"
            return self.db_manager.fetch_dataframe(query, (field_value,))
            
    def add(self, record: Dict[str, Any]) -> int:
        """Add a new record
        
        Args:
            record: Record data as dictionary
            
        Returns:
            int: New record ID
        """
        with self.db_manager:
            columns = ", ".join(record.keys())
            placeholders = ", ".join(["?"] * len(record))
            query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})"
            
            self.db_manager.execute(query, tuple(record.values()))
            self.db_manager.commit()
            
            return self.db_manager.cursor.lastrowid
            
    def bulk_add(self, records: pd.DataFrame) -> bool:
        """Add multiple records
        
        Args:
            records: DataFrame containing records
            
        Returns:
            bool: True if successful
        """
        with self.db_manager:
            columns = ", ".join(records.columns)
            placeholders = ", ".join(["?"] * len(records.columns))
            query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})"
            
            records_list = records.to_records(index=False)
            records_tuples = [tuple(record) for record in records_list]
            
            self.db_manager.executemany(query, records_tuples)
            self.db_manager.commit()
            
            return True
            
    def update(self, record_id: int, record: Dict[str, Any]) -> bool:
        """Update a record
        
        Args:
            record_id: Record ID
            record: Updated record data
            
        Returns:
            bool: True if successful
        """
        with self.db_manager:
            set_clause = ", ".join([f"{key} = ?" for key in record.keys()])
            query = f"UPDATE {self.table_name} SET {set_clause} WHERE id = ?"
            
            params = list(record.values())
            params.append(record_id)
            
            self.db_manager.execute(query, params)
            self.db_manager.commit()
            
            return self.db_manager.cursor.rowcount > 0
            
    def delete(self, record_id: int) -> bool:
        """Delete a record
        
        Args:
            record_id: Record ID
            
        Returns:
            bool: True if successful
        """
        with self.db_manager:
            query = f"DELETE FROM {self.table_name} WHERE id = ?"
            self.db_manager.execute(query, (record_id,))
            self.db_manager.commit()
            
            return self.db_manager.cursor.rowcount > 0
            
    def count(self) -> int:
        """Count records in the table
        
        Returns:
            int: Record count
        """
        with self.db_manager:
            query = f"SELECT COUNT(*) FROM {self.table_name}"
            result = self.db_manager.fetch_one(query)
            return result[0] if result else 0 