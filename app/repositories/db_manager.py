import sqlite3
import os
import pandas as pd
import logging
from config.config import Config

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Manages database connections and operations"""
    
    def __init__(self, db_path=None):
        """Initialize the database manager
        
        Args:
            db_path: Optional path to the database file. If not provided, uses the configured path.
        """
        self.db_path = db_path or Config.DB.SQLITE_PATH
        self.connection = None
        self.cursor = None
        
    def __enter__(self):
        """Context manager entry point - opens the database connection"""
        self.connect()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit point - closes the database connection"""
        self.close()
        
    def connect(self):
        """Connect to the SQLite database"""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.cursor = self.connection.cursor()
            return self.connection
        except sqlite3.Error as e:
            logger.error(f"Error connecting to database: {e}")
            raise
            
    def close(self):
        """Close the database connection"""
        if self.connection:
            self.connection.close()
            self.connection = None
            self.cursor = None
            
    def commit(self):
        """Commit changes to the database"""
        if self.connection:
            self.connection.commit()
            
    def execute(self, query, params=None):
        """Execute a query
        
        Args:
            query: SQL query string
            params: Parameters for the query
            
        Returns:
            cursor: Database cursor
        """
        try:
            if params:
                return self.cursor.execute(query, params)
            else:
                return self.cursor.execute(query)
        except sqlite3.Error as e:
            logger.error(f"Error executing query: {e}")
            logger.error(f"Query: {query}")
            logger.error(f"Params: {params}")
            raise
            
    def executemany(self, query, params_list):
        """Execute a query with multiple parameter sets
        
        Args:
            query: SQL query string
            params_list: List of parameter tuples
            
        Returns:
            cursor: Database cursor
        """
        try:
            return self.cursor.executemany(query, params_list)
        except sqlite3.Error as e:
            logger.error(f"Error executing batch query: {e}")
            raise
            
    def fetch_all(self, query, params=None):
        """Execute a query and fetch all results
        
        Args:
            query: SQL query string
            params: Parameters for the query
            
        Returns:
            list: List of result rows
        """
        self.execute(query, params)
        return self.cursor.fetchall()
        
    def fetch_one(self, query, params=None):
        """Execute a query and fetch one result
        
        Args:
            query: SQL query string
            params: Parameters for the query
            
        Returns:
            tuple: Result row
        """
        self.execute(query, params)
        return self.cursor.fetchone()
        
    def fetch_dataframe(self, query, params=None):
        """Execute a query and return results as a pandas DataFrame
        
        Args:
            query: SQL query string
            params: Parameters for the query
            
        Returns:
            DataFrame: Query results
        """
        try:
            if self.connection is None:
                self.connect()
                
            if params:
                df = pd.read_sql_query(query, self.connection, params=params)
            else:
                df = pd.read_sql_query(query, self.connection)
                
            return df
        except (sqlite3.Error, pd.io.sql.DatabaseError) as e:
            logger.error(f"Error fetching dataframe: {e}")
            raise
            
    def table_exists(self, table_name):
        """Check if a table exists in the database
        
        Args:
            table_name: Name of the table to check
            
        Returns:
            bool: True if table exists, False otherwise
        """
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name=?"
        result = self.fetch_one(query, (table_name,))
        return result is not None
        
    def create_table(self, table_name, columns):
        """Create a table if it doesn't exist
        
        Args:
            table_name: Name of the table to create
            columns: Column definitions as a string
        """
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
        self.execute(query)
        self.commit()
        
    def initialize_database(self):
        """Initialize the database with required tables"""
        # ESG table
        self.create_table(
            Config.DB.ESG_TABLE,
            """
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client TEXT NOT NULL,
            fields TEXT NOT NULL,
            data_type TEXT,
            data_source TEXT,
            sedol_count INTEGER,
            isin_count INTEGER,
            cusip_count INTEGER,
            compliance TEXT
            """
        )
        
        # Shariah DataFeed table
        self.create_table(
            Config.DB.SHARIAH_TABLE,
            """
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client TEXT NOT NULL,
            current_source TEXT,
            after_migration TEXT,
            delivery_name TEXT, 
            fields TEXT,
            universe TEXT,
            universe_count INTEGER,
            frequency TEXT,
            migration_plan TEXT,
            sedol_count INTEGER,
            isin_count INTEGER,
            cusip_count INTEGER
            """
        )
        
        logger.info("Database initialized successfully") 