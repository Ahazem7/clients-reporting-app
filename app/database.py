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

def init_sample_data():
    """Initialize the database with sample data for demo purposes
    This is particularly useful for Streamlit Cloud deployment
    """
    # This function now does nothing to prevent auto-populating tables
    # It's kept for compatibility with existing code
    logger = logging.getLogger(__name__)
    logger.info("Sample data initialization is disabled")
    return

def load_sample_esg_data():
    """
    Manually load sample ESG data
    """
    logger = logging.getLogger(__name__)
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Sample ESG data
        esg_data = [
            ("Clarity", "NPIN", "L, N, G", "FactSet", 0, 0, 0, "Pass"),
            ("Datia", "NPIN, Carbonfoot print, Metric Intensity", "%, Numeric, Numeric", "FactSet, Reuters", 0, 0, 0, "Pass"),
            ("JP Morgan", "NPIN, Carbonfoot print, Metric Intensity", "%, Numeric, Numeric", "FactSet, Reuters", 30000, 30000, 30000, "Pass"),
            ("PWC", "NPIN, Carbonfoot print, Metric Intensity", "%, Numeric, Numeric", "FactSet, Reuters", 30000, 30000, 30000, "Pass"),
            ("Northern Trust", "NPIN, Metric Intensity", "%, Numeric", "FactSet, Reuters", 30000, 30000, 30000, "Pass"),
            ("Owlshares", "NPIN, Carbonfoot print, Metric Intensity", "%, Numeric, Numeric", "FactSet, Reuters", 0, 0, 0, "Pass"),
            ("State Street", "NPIN, Carbonfoot print, Metric Intensity", "%, Numeric, Numeric", "FactSet, Reuters", 30000, 30000, 30000, "Pass"),
            ("Blueonion", "NPIN, Carbonfoot print, Metric Intensity", "%, Numeric, Numeric", "FactSet, Reuters", 0, 0, 0, "Pass"),
            ("Covalence", "NPIN, Carbonfoot print, Metric Intensity", "%, Numeric, Numeric", "FactSet, Reuters", 0, 0, 0, "Pass"),
            ("GIB", "E,S,G", "Text", "FactSet", 0, 0, 0, "Pass")
        ]
        
        cursor.executemany(f"""
            INSERT INTO {Config.DB.ESG_TABLE} (client, fields, data_type, data_source, sedol_count, isin_count, cusip_count, compliance)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, esg_data)
        conn.commit()
        logger.info(f"Added {len(esg_data)} sample ESG records")
        
    except sqlite3.Error as e:
        logger.error(f"Error loading sample ESG data: {e}")
        raise
    finally:
        if conn:
            conn.close()

def load_sample_shariah_data():
    """
    Manually load sample Shariah data
    """
    logger = logging.getLogger(__name__)
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Sample Shariah data
        shariah_data = [
            ("Acadian", "Reuters", "", "Acadian - AlRajhi Delivery", "ISIN, Ticker, Name", "Global", 23000, "Quarterly", "", 10000, 10000, 10000),
            ("ADIB", "Reuters", "", "ADIB SAUDI", "Name, ISIN, Ticker, Sector, Market Cap", "SAUDI", 1700, "Quarterly", "", 0, 0, 0),
            ("Aghaz", "Factset", "Factset", "Aghaz", "ISIN, Ticker, Name, Sector", "US", 1270, "Quarterly", "1st of February", 0, 0, 0),
            ("Al Rajhi", "Reuters", "", "AlRajhi Egypt", "Ticker, ISIN, Name, Nation, Sector", "EGYPT", 28000, "Quarterly", "", 0, 0, 0),
            ("Al Salam", "Factset", "", "AlSalam Bank", "Name, Ticker, Exchanges Code, AAOIFI", "USA, UK", 12900, "Quarterly", "", 0, 0, 0),
            ("AlBilad", "Reuters", "", "Al Bilad Saudi Delivery", "Name, Nation, Ticker", "Saudi", 9950, "Quarterly", "", 0, 0, 0),
            ("Alinma", "Reuters", "", "Alinma Brokerage List", "Name, Nation, ISIN, Ticker", "Global", 19000, "Monthly", "", 0, 0, 0),
            ("AlJazira", "Reuters", "", "Aljazira Symbols", "ISIN, Ticker, Name, Exchanges", "MENA & US", 5300, "Monthly", "", 0, 0, 0),
            ("Alpha Capital", "Factset", "Factset", "Alpha Capital Delivery", "Name, ISIN, Ticker", "SAUDI,GCC", 570, "Quarterly", "1st of January", 0, 0, 0),
            ("Arabesque", "Reuters", "", "Arabesque", "ISIN, SEDOL, Ticker, FIGI, Nation, Name", "Global", 36000, "Monthly", "", 10000, 10000, 10000)
        ]
        
        cursor.executemany(f"""
            INSERT INTO {Config.DB.SHARIAH_TABLE} (client, current_source, after_migration, delivery_name, fields, universe, universe_count, frequency, migration_plan, sedol_count, isin_count, cusip_count)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, shariah_data)
        conn.commit()
        logger.info(f"Added {len(shariah_data)} sample Shariah records")
        
    except sqlite3.Error as e:
        logger.error(f"Error loading sample Shariah data: {e}")
        raise
    finally:
        if conn:
            conn.close() 