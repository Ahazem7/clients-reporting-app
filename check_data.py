import sqlite3
import logging
import sys
sys.path.insert(0, '.')
from app.config import Config

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_data():
    try:
        conn = sqlite3.connect(Config.DATABASE_PATH)
        cursor = conn.cursor()
        
        # Get database name
        logger.info(f"Checking database: {Config.DATABASE_PATH}")
        
        # Check Shariah table
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {Config.DB.SHARIAH_TABLE}")
            shariah_count = cursor.fetchone()[0]
            logger.info(f"{Config.DB.SHARIAH_TABLE} records count: {shariah_count}")
            
            # Show specific data if available
            if shariah_count > 0:
                cursor.execute(f"SELECT client FROM {Config.DB.SHARIAH_TABLE} LIMIT 3")
                samples = cursor.fetchall()
                logger.info(f"Sample clients: {', '.join([s[0] for s in samples])}")
            
        except sqlite3.Error as e:
            logger.error(f"Error checking {Config.DB.SHARIAH_TABLE} table: {e}")
            
        # Check ESG table
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {Config.DB.ESG_TABLE}")
            esg_count = cursor.fetchone()[0]
            logger.info(f"{Config.DB.ESG_TABLE} records count: {esg_count}")
            
            # Show specific data if available
            if esg_count > 0:
                cursor.execute(f"SELECT client FROM {Config.DB.ESG_TABLE} LIMIT 3")
                samples = cursor.fetchall()
                logger.info(f"Sample clients: {', '.join([s[0] for s in samples])}")
                
        except sqlite3.Error as e:
            logger.error(f"Error checking {Config.DB.ESG_TABLE} table: {e}")
            
    except sqlite3.Error as e:
        logger.error(f"Error connecting to database: {e}")
    finally:
        if 'conn' in locals() and conn:
            conn.close()
    
    logger.info("Data check completed")

if __name__ == "__main__":
    check_data() 