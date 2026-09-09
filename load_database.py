import pandas as pd
import sqlite3
from pathlib import Path

DB = "bluestock_mf.db"
DATA = Path("data/processed")

conn = sqlite3.connect(DB)


# 1. Scheme Performance → fact_performance
df = pd.read_csv(DATA / "scheme_performance_cleaned.csv")

if "expense_ratio_anomaly" in df.columns:
    df = df.drop(columns=["expense_ratio_anomaly"])

df.to_sql("fact_performance", conn, if_exists="append", index=False)
print("fact_performance loaded:", len(df))


# 2. AUM → fact_aum
df = pd.read_csv(DATA / "aum_by_fund_house_cleaned.csv")

df.to_sql("fact_aum", conn, if_exists="append", index=False)
print("fact_aum loaded:", len(df))


# 3. Create date dimension
dates = set()

for file, column in [
    ("nav_history_cleaned.csv", "date"),
    ("investor_transactions_cleaned.csv", "transaction_date"),
    ("aum_by_fund_house_cleaned.csv", "date")
]:
    df = pd.read_csv(DATA / file)

    dates.update(
        pd.to_datetime(
            df[column],
            errors="coerce"
        ).dropna().dt.date
    )


date_df = pd.DataFrame({"date": sorted(dates)})

date_df["year"] = pd.to_datetime(date_df["date"]).dt.year
date_df["month"] = pd.to_datetime(date_df["date"]).dt.month
date_df["month_name"] = pd.to_datetime(date_df["date"]).dt.month_name()
date_df["quarter"] = pd.to_datetime(date_df["date"]).dt.quarter

date_df.to_sql(
    "dim_date",
    conn,
    if_exists="append",
    index=False
)

print("dim_date loaded:", len(date_df))


conn.commit()

print("\nDatabase loading completed successfully!")

conn.close()