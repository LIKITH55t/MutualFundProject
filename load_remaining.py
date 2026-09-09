import pandas as pd
import sqlite3
from pathlib import Path

DB = "bluestock_mf.db"
DATA = Path("data/processed")

conn = sqlite3.connect(DB)

files = {
    "portfolio_holdings_cleaned.csv": "portfolio_holdings",
    "benchmark_indices_cleaned.csv": "benchmark_indices",
    "monthly_sip_inflows_cleaned.csv": "monthly_sip_inflows",
    "category_inflows_cleaned.csv": "category_inflows",
    "industry_folio_count_cleaned.csv": "industry_folio_count"
}

for file, table in files.items():
    df = pd.read_csv(DATA / file)

    # Remove auto-generated date index conflicts if present
    df.to_sql(table, conn, if_exists="append", index=False)

    print(f"{table} loaded: {len(df)}")

conn.commit()
conn.close()

print("\nAll remaining datasets loaded successfully!")