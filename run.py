import os
import subprocess
import sys
import platform

def main():
    """
    Run the Streamlit application with proper initialization
    """
    print("Starting Clients Reporting App...")
    
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Set environment variables if needed
    os.environ["PYTHONPATH"] = current_dir
    
    # Check if we need to install requirements
    if not os.path.exists(os.path.join(current_dir, "venv")):
        create_venv = input("Virtual environment not found. Create one? (y/n): ").lower()
        if create_venv == "y":
            print("Creating virtual environment...")
            
            # Create virtual environment
            if platform.system() == "Windows":
                subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
                pip_cmd = os.path.join(current_dir, "venv", "Scripts", "pip")
            else:
                subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
                pip_cmd = os.path.join(current_dir, "venv", "bin", "pip")
            
            # Install requirements
            print("Installing requirements...")
            subprocess.run([pip_cmd, "install", "-r", "requirements.txt"], check=True)
        else:
            print("Please install the required packages listed in requirements.txt")
    
    # Decide which python to use
    if os.path.exists(os.path.join(current_dir, "venv")):
        if platform.system() == "Windows":
            python_cmd = os.path.join(current_dir, "venv", "Scripts", "python")
        else:
            python_cmd = os.path.join(current_dir, "venv", "bin", "python")
    else:
        python_cmd = sys.executable
    
    # Run the streamlit app
    streamlit_cmd = [python_cmd, "-m", "streamlit", "run", "app/main.py"]
    subprocess.run(streamlit_cmd, check=True)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nApplication stopped.")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1) 