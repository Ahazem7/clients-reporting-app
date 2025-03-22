import os
from app.config import Config
from app.utils.logging_setup import setup_logging
from app.database import init_db

# Ensure necessary directories exist
def init_app():
    """Initialize application by creating required directories and database"""
    # Create directories if they don't exist
    os.makedirs(os.path.dirname(Config.DATABASE_PATH), exist_ok=True)
    os.makedirs(Config.LOG_DIR, exist_ok=True)
    
    # Initialize logging
    setup_logging()
    
    # Initialize database
    init_db()

# Initialize the application when imported
init_app() 