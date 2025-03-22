import os
from pathlib import Path

# Base directory of the project
BASE_DIR = Path(__file__).parent.parent

# Database configurations
class DatabaseConfig:
    # Default to SQLite for development, can be overridden for production
    DB_TYPE = os.getenv("DB_TYPE", "sqlite")
    DB_NAME = os.getenv("DB_NAME", "data.db")
    DB_HOST = os.getenv("DB_HOST", "")
    DB_USER = os.getenv("DB_USER", "")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_PORT = os.getenv("DB_PORT", "")
    
    # SQLite specific
    SQLITE_PATH = os.path.join(BASE_DIR, DB_NAME)
    
    # Table names
    ESG_TABLE = "esg_data"
    SHARIAH_TABLE = "shariah_datafeed"
    
    @classmethod
    def get_connection_string(cls):
        """Get the appropriate database connection string based on configuration"""
        if cls.DB_TYPE.lower() == "sqlite":
            return f"sqlite:///{cls.SQLITE_PATH}"
        elif cls.DB_TYPE.lower() == "postgresql":
            return f"postgresql://{cls.DB_USER}:{cls.DB_PASSWORD}@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}"
        else:
            raise ValueError(f"Unsupported database type: {cls.DB_TYPE}")

# Application configurations
class AppConfig:
    DEBUG = os.getenv("DEBUG", "True").lower() in ("true", "1", "t")
    TESTING = os.getenv("TESTING", "False").lower() in ("true", "1", "t")
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_key_change_in_production")
    
    # Streamlit specific settings
    STREAMLIT_SERVER_PORT = int(os.getenv("STREAMLIT_SERVER_PORT", "8501"))
    STREAMLIT_SERVER_HEADLESS = os.getenv("STREAMLIT_SERVER_HEADLESS", "False").lower() in ("true", "1", "t")
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.path.join(BASE_DIR, "app.log")

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    env_path = os.path.join(BASE_DIR, '.env')
    if os.path.exists(env_path):
        load_dotenv(env_path)
except ImportError:
    pass  # python-dotenv not installed

# Combine all configs into a single class for easy access
class Config:
    DB = DatabaseConfig
    APP = AppConfig 