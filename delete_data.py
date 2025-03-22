import sqlite3
import logging
import sys
sys.path.insert(0, '.')
from app.config import Config

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def delete_shariah_data():
    try:
        conn = sqlite3.connect(Config.DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM {Config.DB.SHARIAH_TABLE}")
        conn.commit()
        logger.info(f"Deleted all records from {Config.DB.SHARIAH_TABLE} table")
        
        # Verify deletion
        cursor.execute(f"SELECT COUNT(*) FROM {Config.DB.SHARIAH_TABLE}")
        count = cursor.fetchone()[0]
        logger.info(f"Shariah records count after deletion: {count}")
        
    except sqlite3.Error as e:
        logger.error(f"Error deleting data: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    delete_shariah_data() 