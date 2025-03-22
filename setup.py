from setuptools import setup, find_packages

setup(
    name="clients-reporting-app",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "streamlit>=1.29.0",
        "pandas>=2.0.0",
        "plotly>=5.17.0",
        "numpy>=1.24.0",
        "python-dotenv>=1.0.0",
    ],
) 