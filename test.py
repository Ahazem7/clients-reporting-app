import streamlit as st
import pandas as pd
import sqlite3
import re

# Database setup
DB_FILE = "data.db"
ESG_TABLE = "esg_data"
SHARIAH_TABLE = "shariah_datafeed"

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # ESG table
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {ESG_TABLE} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client TEXT NOT NULL,
            fields TEXT NOT NULL,
            data_type TEXT,
            data_source TEXT,
            sedol_count INTEGER,
            isin_count INTEGER,
            cusip_count INTEGER,
            compliance TEXT
        )
    """)

    # Shariah DataFeed table
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {SHARIAH_TABLE} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client TEXT NOT NULL,
            fields TEXT NOT NULL,
            universe TEXT,
            universe_count INTEGER,
            frequency TEXT,
            sedol_count INTEGER,
            isin_count INTEGER,
            cusip_count INTEGER,
            data_source TEXT
        )
    """)

    conn.commit()
    conn.close()

# Load data from the database
def load_data(table):
    conn = sqlite3.connect(DB_FILE)
    query = f"SELECT * FROM {table}"
    data = pd.read_sql_query(query, conn)
    conn.close()
    return data

# Save new data to the database
def save_data(table, new_entry):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    columns = ", ".join([f'"{col}"' for col in new_entry.keys()])  # Quote column names
    placeholders = ", ".join(["?"] * len(new_entry))
    cursor.execute(f"INSERT INTO {table} ({columns}) VALUES ({placeholders})", tuple(new_entry.values()))
    conn.commit()
    conn.close()

# Bulk insert data into the database
def bulk_insert_data(table, data):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    columns = ", ".join([f'"{col}"' for col in data.columns])  # Quote column names
    placeholders = ", ".join(["?"] * len(data.columns))
    cursor.executemany(
        f"INSERT INTO {table} ({columns}) VALUES ({placeholders})",
        data.to_records(index=False)  # Convert DataFrame to iterable of tuples
    )
    conn.commit()
    conn.close()

# Delete data from the database
def delete_data(table, row_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM {table} WHERE id = ?", (row_id,))
    conn.commit()
    conn.close()

# Normalize and deduplicate text fields
def strict_deduplicate_all_fields(field_series):
    seen = set()
    preserved_order = []
    for entry in field_series.dropna().unique():
        for sub_entry in re.split(r",|\s+", entry):
            cleaned_entry = " ".join(sub_entry.split()).strip()
            if cleaned_entry.lower() not in seen:
                seen.add(cleaned_entry.lower())
                preserved_order.append(cleaned_entry)
    return ", ".join(preserved_order)

# Initialize the database
init_db()

# Streamlit App
st.title("Data Management System")

# Sidebar Navigation
section = st.sidebar.radio("Navigate", ["Inputs", "Base Data", "Aggregation"])

if section == "Inputs":
    st.header("Inputs")
    input_section = st.sidebar.radio("Select Input Section", ["ESG Inputs", "Shariah DataFeed Inputs", "Bulk Upload"])

    if input_section == "ESG Inputs":
        st.subheader("Add New ESG Data")
        with st.form("esg_form"):
            client = st.text_input("Client Name")
            fields = st.text_area("Fields (separate by commas)")
            data_type = st.text_input("Data Type (e.g., Numeric, Percentage)")
            data_source = st.text_input("Data Source (e.g., FactSet, Reuters)")
            sedol_count = st.number_input("SEDOL Count", min_value=0, step=1)
            isin_count = st.number_input("ISIN Count", min_value=0, step=1)
            cusip_count = st.number_input("CUSIP Count", min_value=0, step=1)
            compliance = st.selectbox("Compliance", ["", "Pass", "Fail", "No"])

            submitted = st.form_submit_button("Submit")

            if submitted:
                if not client or not fields or not data_source:
                    st.error("Please fill out all required fields: Client, Fields, and Data Source.")
                else:
                    new_entry = {
                        "client": client,
                        "fields": fields,
                        "data_type": data_type,
                        "data_source": data_source,
                        "sedol_count": sedol_count,
                        "isin_count": isin_count,
                        "cusip_count": cusip_count,
                        "compliance": compliance
                    }
                    save_data(ESG_TABLE, new_entry)
                    st.success("Data added successfully!")

    elif input_section == "Shariah DataFeed Inputs":
        st.subheader("Add New Shariah DataFeed Data")
        with st.form("shariah_form"):
            client = st.text_input("Client Name")
            fields = st.text_area("Fields (separate by commas)")
            universe = st.text_input("Universe")
            universe_count = st.number_input("Universe Count", min_value=0, step=1)
            frequency = st.text_input("Frequency")
            sedol_count = st.number_input("SEDOL Count", min_value=0, step=1)
            isin_count = st.number_input("ISIN Count", min_value=0, step=1)
            cusip_count = st.number_input("CUSIP Count", min_value=0, step=1)
            data_source = st.text_area("Data Source (separate by commas)")

            submitted = st.form_submit_button("Submit")

            if submitted:
                if not client or not fields:
                    st.error("Please fill out all required fields: Client and Fields.")
                else:
                    new_entry = {
                        "client": client,
                        "fields": fields,
                        "universe": universe,
                        "universe_count": universe_count,
                        "frequency": frequency,
                        "sedol_count": sedol_count,
                        "isin_count": isin_count,
                        "cusip_count": cusip_count,
                        "data_source": data_source
                    }
                    save_data(SHARIAH_TABLE, new_entry)
                    st.success("Data added successfully!")

    elif input_section == "Bulk Upload":
        st.subheader("Bulk Upload Data")
        uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])
        if uploaded_file:
            data = pd.ExcelFile(uploaded_file)

            if st.checkbox("Upload ESG Data"):
                esg_data = data.parse(sheet_name="ESG Data")
                esg_data_cleaned = esg_data.rename(columns={
                    "Client": "client",
                    "Fields": "fields",
                    "Data Type": "data_type",
                    "Data Source": "data_source",
                    "SEDOL Count": "sedol_count",
                    "ISIN Count": "isin_count",
                    "CUSIP Count": "cusip_count",
                    "Compliance": "compliance"
                }).dropna(subset=["client", "fields"])
                bulk_insert_data(ESG_TABLE, esg_data_cleaned)
                st.success("ESG Data uploaded successfully!")

            if st.checkbox("Upload Shariah DataFeed Data"):
                shariah_data = data.parse(sheet_name="Shariah DataFeed")
                shariah_data_cleaned = shariah_data.rename(columns={
                    "Client": "client",
                    "Fields": "fields",
                    "Universe": "universe",
                    "Universe Count": "universe_count",
                    "Frequency": "frequency",
                    "SEDOL Count": "sedol_count",
                    "ISIN Count": "isin_count",
                    "CUSIP Count": "cusip_count",
                    "Data Source": "data_source"
                }).dropna(subset=["client", "fields"])
                bulk_insert_data(SHARIAH_TABLE, shariah_data_cleaned)
                st.success("Shariah DataFeed Data uploaded successfully!")

elif section == "Base Data":
    st.header("Base Data")
    base_data_section = st.sidebar.radio("Select Base Data Section", ["ESG Base Data", "Shariah DataFeed Base Data"])

    if base_data_section == "ESG Base Data":
        esg_data = load_data(ESG_TABLE)
        st.subheader("ESG Base Data")
        st.dataframe(esg_data)

    elif base_data_section == "Shariah DataFeed Base Data":
        shariah_data = load_data(SHARIAH_TABLE)
        st.subheader("Shariah DataFeed Base Data")
        st.dataframe(shariah_data)

elif section == "Aggregation":
    st.header("Aggregation")
    aggregation_section = st.sidebar.radio("Select Aggregation Section", ["ESG Aggregation", "Shariah DataFeed Aggregation"])

    if aggregation_section == "ESG Aggregation":
        esg_data = load_data(ESG_TABLE)
        if not esg_data.empty:
            esg_aggregated = esg_data.groupby("client").agg({
                "fields": lambda x: strict_deduplicate_all_fields(x),
                "data_source": lambda x: strict_deduplicate_all_fields(x),
                "sedol_count": lambda x: ", ".join(map(str, sorted(set(x.dropna())))),
                "isin_count": lambda x: ", ".join(map(str, sorted(set(x.dropna())))),
                "cusip_count": lambda x: ", ".join(map(str, sorted(set(x.dropna()))))
            }).reset_index()

            # Adjust delivery count to reflect unique rows
            esg_aggregated["delivery_count"] = esg_data.groupby("client").size().reset_index(name="delivery_count")["delivery_count"]

            st.subheader("ESG Aggregated Data")
            st.dataframe(esg_aggregated)
        else:
            st.info("No ESG data available for aggregation.")

    elif aggregation_section == "Shariah DataFeed Aggregation":
        shariah_data = load_data(SHARIAH_TABLE)
        if not shariah_data.empty:
            shariah_aggregated = shariah_data.groupby("client").agg({
                "fields": lambda x: strict_deduplicate_all_fields(x),
                "universe": lambda x: strict_deduplicate_all_fields(x),
                "universe_count": lambda x: ", ".join(map(str, sorted(set(x.dropna())))),
                "frequency": lambda x: strict_deduplicate_all_fields(x),
                "sedol_count": lambda x: ", ".join(map(str, sorted(set(x.dropna())))),
                "isin_count": lambda x: ", ".join(map(str, sorted(set(x.dropna())))),
                "cusip_count": lambda x: ", ".join(map(str, sorted(set(x.dropna())))),
                "data_source": lambda x: strict_deduplicate_all_fields(x)
            }).reset_index()

            # Adjust delivery count to reflect unique rows
            shariah_aggregated["delivery_count"] = shariah_data.groupby("client").size().reset_index(name="delivery_count")["delivery_count"]

            st.subheader("Shariah DataFeed Aggregated Data")
            st.dataframe(shariah_aggregated)
        else:
            st.info("No Shariah DataFeed data available for aggregation.")
