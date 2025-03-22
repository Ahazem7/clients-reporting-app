import sqlite3
import os
import logging
from app.config import Config

logger = logging.getLogger(__name__)

def get_connection():
    """Get a connection to the database
    
    Returns:
        sqlite3.Connection: Database connection
    """
    db_path = Config.DATABASE_PATH
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    try:
        conn = sqlite3.connect(db_path)
        return conn
    except sqlite3.Error as e:
        logger.error(f"Error connecting to database: {e}")
        raise

def init_db():
    """Initialize the database with required tables"""
    db_path = Config.DATABASE_PATH
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create ESG table
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {Config.DB.ESG_TABLE} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client TEXT NOT NULL,
                fields TEXT NOT NULL,
                data_type TEXT,
                data_source TEXT,
                sedol_count INTEGER,
                isin_count INTEGER,
                cusip_count INTEGER,
                compliance TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create Shariah DataFeed table
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {Config.DB.SHARIAH_TABLE} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client TEXT NOT NULL,
                fields TEXT,
                data_type TEXT,
                data_source TEXT,
                sedol_count INTEGER,
                isin_count INTEGER,
                cusip_count INTEGER,
                compliance TEXT,
                frequency TEXT,
                current_source TEXT,
                after_migration TEXT,
                delivery_name TEXT, 
                universe TEXT,
                universe_count INTEGER,
                migration_plan TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        logger.info("Database initialized successfully")
    except sqlite3.Error as e:
        logger.error(f"Error initializing database: {e}")
        raise
    finally:
        if conn:
            conn.close() 