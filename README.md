# Clients Reporting App

A Streamlit-based application for tracking and managing ESG and Shariah DataFeed client information.

## Features

- Dashboard with data analytics and visualizations
- Input forms for ESG and Shariah DataFeed data
- Bulk data import functionality
- Data viewing with filtering capabilities
- Record editing functionality
- Aggregated data reports

## Project Structure

```
app/
├── config.py              # Application configuration
├── database.py            # Database connection and schema
├── main.py                # Main application entry point
├── models/                # Data models
│   ├── __init__.py
│   ├── esg.py             # ESG data model
│   └── shariah.py         # Shariah data model
├── services/              # Business logic services
│   ├── __init__.py
│   ├── esg_service.py     # ESG data service
│   └── shariah_service.py # Shariah data service
├── ui/                    # User interface components
│   ├── components/        # Reusable UI components
│   │   ├── esg_form.py    # ESG input forms
│   │   ├── esg_view.py    # ESG data views
│   │   ├── shariah_form.py# Shariah input forms
│   │   ├── shariah_view.py# Shariah data views
│   │   └── ui_helpers.py  # Shared UI utilities
│   └── pages/             # Application pages
│       ├── dashboard_page.py  # Dashboard page
│       ├── edit_page.py       # Data editing page
│       ├── inputs_page.py     # Data input page
│       └── view_page.py       # Data viewing page
└── utils/                 # Utility functions
    ├── __init__.py
    ├── data_helpers.py    # Data manipulation utilities
    └── logging_setup.py   # Logging configuration
```

## Installation

1. Clone the repository
2. Create a virtual environment
3. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the application with:

```
streamlit run app/main.py
```

## Dependencies

- Python 3.8+
- Streamlit
- Pandas
- Plotly
- SQLite (via sqlite3)

## Development

To add new features:

1. Create the appropriate model in the `models` directory
2. Implement the necessary business logic in the `services` directory
3. Add UI components in the `ui/components` directory
4. Update or create pages in the `ui/pages` directory as needed

## License

MIT 