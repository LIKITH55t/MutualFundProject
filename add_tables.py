import sqlite3

DB = "bluestock_mf.db"

conn = sqlite3.connect(DB)

schema = """
CREATE TABLE IF NOT EXISTS portfolio_holdings (
    holding_id INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code INTEGER,
    stock_symbol TEXT,
    stock_name TEXT,
    sector TEXT,
    weight_pct REAL,
    market_value_cr REAL,
    current_price_inr REAL,
    portfolio_date DATE
);

CREATE TABLE IF NOT EXISTS benchmark_indices (
    benchmark_id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE,
    index_name TEXT,
    close_value REAL
);

CREATE TABLE IF NOT EXISTS monthly_sip_inflows (
    month DATE PRIMARY KEY,
    sip_inflow_crore REAL,
    active_sip_accounts_crore REAL,
    new_sip_accounts_lakh REAL,
    sip_aum_lakh_crore REAL,
    yoy_growth_pct REAL
);

CREATE TABLE IF NOT EXISTS category_inflows (
    category_inflow_id INTEGER PRIMARY KEY AUTOINCREMENT,
    month DATE,
    category TEXT,
    net_inflow_crore REAL
);

CREATE TABLE IF NOT EXISTS industry_folio_count (
    month DATE PRIMARY KEY,
    total_folios_crore REAL,
    equity_folios_crore REAL,
    debt_folios_crore REAL,
    hybrid_folios_crore REAL,
    others_folios_crore REAL
);
"""

conn.executescript(schema)
conn.commit()

print("5 additional tables created successfully.")

cursor = conn.cursor()
cursor.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type='table'
    ORDER BY name
""")

print("\nTables:")
for table in cursor.fetchall():
    print("-", table[0])

conn.close()