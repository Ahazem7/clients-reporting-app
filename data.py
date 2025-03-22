import sqlite3

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
            current_source TEXT,
            after_migration TEXT,
            delivery_name TEXT,
            fields TEXT,
            universe TEXT,
            universe_count INTEGER,
            frequency TEXT,
            migration_plan TEXT,
            sedol_count INTEGER,
            isin_count INTEGER,
            cusip_count INTEGER
        )
    """)

    # Pre-populate ESG data
    esg_data = [
        ("Clarity", "NPIN", "L, N, G", "FactSet", "FactSet: NPIN", 0, 0, 0, "Pass"),
        ("Datia", "NPIN, Carbonfoot print, Metric Intensity", "%, Numeric, Numeric", "FactSet, Reuters", "FactSet: NPIN & Qual, Reuters: Metric", 0, 0, 0, "Pass"),
        ("JP Morgan", "NPIN, Carbonfoot print, Metric Intensity", "%, Numeric, Numeric", "FactSet, Reuters", "FactSet: NPIN & Qual, Reuters: Metric", 30000, 30000, 30000, "Pass"),
        ("PWC", "NPIN, Carbonfoot print, Metric Intensity", "%, Numeric, Numeric", "FactSet, Reuters", "FactSet: NPIN & Qual, Reuters: Metric", 30000, 30000, 30000, "Pass"),
        ("Northern Trust", "NPIN, Metric Intensity", "%, Numeric", "FactSet, Reuters", "FactSet: NPIN & Qual, Reuters: Metric", 30000, 30000, 30000, "Pass"),
        ("Owlshares", "NPIN, Carbonfoot print, Metric Intensity", "%, Numeric, Numeric", "FactSet, Reuters", "FactSet: NPIN & Qual, Reuters: Metric", 0, 0, 0, "Pass"),
        ("State Street", "NPIN, Carbonfoot print, Metric Intensity", "%, Numeric, Numeric", "FactSet, Reuters", "FactSet: NPIN & Qual, Reuters: Metric", 30000, 30000, 30000, "Pass"),
        ("Blueonion", "NPIN, Carbonfoot print, Metric Intensity", "%, Numeric, Numeric", "FactSet, Reuters", "FactSet: NPIN & Qual, Reuters: Metric", 0, 0, 0, "Pass"),
        ("Covalence", "NPIN, Carbonfoot print, Metric Intensity", "%, Numeric, Numeric", "FactSet, Reuters", "FactSet: NPIN & Qual, Reuters: Metric", 0, 0, 0, "Pass"),
        ("GIB", "E,S,G", "Text", "FactSet", "FactSet: NPIN", 0, 0, 0, "Pass")
    ]
    cursor.executemany(f"""
        INSERT INTO {ESG_TABLE} (client, fields, data_type, data_source, sedol_count, isin_count, cusip_count, compliance)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, esg_data)

    # Pre-populate Shariah DataFeed data
    shariah_data = [
        ("Acadian", "Reuters", "", "Acadian - AlRajhi Delivery", "ISIN, Ticker, Name", "Global", 23000, "Quarterly", "", 10000, 10000, 10000),
        ("ADIB", "Reuters", "", "ADIB SAUDI", "Name, ISIN, Ticker, Sector, Market Cap", "SAUDI", 1700, "Quarterly", "", 0, 0, 0),
        ("Aghaz", "Factset", "Factset", "Aghaz", "ISIN, Ticker, Name, Sector", "US", 1270, "Quarterly", "1st of February", 0, 0, 0),
        ("Al Rajhi", "Reuters", "", "AlRajhi Egypt", "Ticker, ISIN, Name, Nation, Sector, Fiscal Period, Al-Rajhi, [Al-Rajhi] Debt Ratio, [Al-Rajhi] Financial Status, [Al-Rajhi] Non Permissible Income Ratio, [Al-Rajhi] NPIN Status, [Al-Rajhi] Preference Share, [Al-Rajhi] Country of Incorporation, Al Rajhi Business Activity, Al Rajhi Brokerage Alternative", "EGYPT", 28000, "Quarterly", "", 0, 0, 0),
        ("Al Salam", "Factset", "", "AlSalam Bank", "Name, Ticker, Exchanges Code, AAOIFI", "USA, France, Germany, United Kingdom, Switzerland, GCC, Japan, and Hong Kong", 12900, "Quarterly", "", 0, 0, 0),
        ("AlBilad", "Reuters", "", "Al Bilad Saudi Delivery", "Name, Nation, Ticker", "Saudi", 9950, "Quarterly", "", 0, 0, 0),
        ("Alinma", "Reuters", "", "Alinma Brokerage List", "Name, Nation, ISIN, Ticker", "Global", 19000, "Monthly", "", 0, 0, 0),
        ("AlJazira", "Reuters", "", "Aljazira Symbols", "ISIN, Ticker, Name, Exchanges, AlJazeera RB1, AlJazeera RB2", "MENA & US", 5300, "Monthly", "", 0, 0, 0),
        ("Alpha Capital", "Factset", "Factset", "Alpha Capital Delivery", "Name, ISIN, Ticker", "SAUDI,GCC", 570, "Quarterly", "1st of January", 0, 0, 0),
        ("Arabesque", "Reuters", "", "Arabesque", "ISIN, SEDOL, Ticker, FIGI, Nation, Name, AAOIFI, Cash and Cash Equivalents - Total (in USD), Assets - Total (in USD), Receivables - Total (in USD), [AAOIFI] Interest bearing Investments, Cash and Short Term Inv. - Conv. (in USD), Cash and Short Term Inv. - Total (in USD), Long Term Inv. - Conv. (in USD), Long Term Inv. - Total (in USD), Note Receivable - Long Term (in USD), Notes Receivable - Short Term (in USD), Trailing 12 Months Market Cap (Daily) (in USD), [AAOIFI] Interest bearing Debts, Debt - Conv. (in USD), Debt - Total (in USD), [AAOIFI] Non permissible Income, [AAOIFI] Preference Share, Dow Jones Islamic based, [Dow Jones Islamic-based] Non permissible Income, [Dow Jones Islamic-based] Interest bearing Investments, [Dow Jones Islamic-based] Interest bearing Debts, [Dow Jones Islamic-based] Liquidity, FTSE Shariah based, [FTSE Shariah-based] Non permissible Income, [FTSE Shariah-based] Interest bearing Investments, [FTSE Shariah-based] Interest bearing Debts, [FTSE Shariah-based] Liquidity, Ideal Ratings, [IdealRatings] NPIN Ratio, [IdealRatings] Interest Bearing Investments Ratio, [IdealRatings] Debt Ratio, [IdealRatings] Screening 3 , MSCI Islamic based, [MSCI Islamic-based] Non permissible Income, [MSCI Islamic-based] Interest bearing Investments, [MSCI Islamic-based] Interest bearing Debts, [MSCI Islamic-based] Liquidity, FTSE Russell Ideal Ratings, [FTSE Russell Ideal Ratings]  Non permissible Income, [FTSE Russell Ideal Ratings]  Interest bearing Ratio, [FTSE Russell Ideal Ratings]  Debt Ratio, [FTSE Russell Ideal Ratings]  Israel, [FTSE Russell Ideal Ratings]  Issue Type, [FTSE Russell Ideal Ratings]  Preference Share, S P Shariah based, [S&P Shariah-based] NPIN Global, [S&P Shariah-based] NPIN GCC, [S&P Shariah-based] Media GCC, [S&P Shariah-based] Interest bearing Investments, [S&P Shariah-based] Interest bearing Debts, [S&P Shariah-based] Liquidity, Malaysia SC, [Malaysia SC] Interest bearing and Non compliant Operations, [Malaysia SC] Investment Financial Services and Real Estate Operations, [Malaysia SC] Interest bearing and Non compliant Operations PBT, [Malaysia SC] Investment Financial services and Real Estate Operations PBT, [Malaysia SC] Interest bearing Debts, [Malaysia SC] Interest bearing Investments, [Malaysia SC]   Preference/Trust Share, Nation Code, Market Cap (in USD), Free Float Shares, Total Common Shares, Sector", "Global", 36000, "Monthly", "", 10000, 10000, 10000)
    ]
    cursor.executemany(f"""
        INSERT INTO {SHARIAH_TABLE} (client, current_source, after_migration, delivery_name, fields, universe, universe_count, frequency, migration_plan, sedol_count, isin_count, cusip_count)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, shariah_data)

    conn.commit()
    conn.close()

# Create the database
init_db()
print("Database created successfully!")
