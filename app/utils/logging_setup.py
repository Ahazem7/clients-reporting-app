import os
import logging
from logging.handlers import RotatingFileHandler
import sys
from app.config import Config

def setup_logging():
    """Set up logging configuration"""
    # Ensure log directory exists
    os.makedirs(os.path.dirname(Config.APP.LOG_FILE), exist_ok=True)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.getLevelName(Config.APP.LOG_LEVEL))
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.getLevelName(Config.APP.LOG_LEVEL))
    console_format = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    console_handler.setFormatter(console_format)
    
    # Create file handler
    file_handler = RotatingFileHandler(
        filename=Config.APP.LOG_FILE,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(logging.getLevelName(Config.APP.LOG_LEVEL))
    file_format = logging.Formatter('%(asctime)s %(levelname)s [%(filename)s:%(lineno)d] %(message)s')
    file_handler.setFormatter(file_format)
    
    # Add handlers to root logger
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    
    # Set up streamlit logging
    logging.getLogger("streamlit").setLevel(logging.WARNING)
    
    logging.info("Logging initialized") 