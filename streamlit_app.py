import os
import sys
import streamlit as st

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Initialize the database with tables and sample data
from app.database import init_db, init_sample_data

# Initialize database
init_db()
init_sample_data()

# Import and run the main application
from app.main import main

# Execute the main function
if __name__ == "__main__":
    main() 