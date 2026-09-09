import pandas as pd
from pathlib import Path

RAW = Path("data/raw")
OUT = Path("data/processed")
OUT.mkdir(parents=True, exist_ok=True)


# 1. Portfolio Holdings
file = RAW / "1788499982117-e3d6ab98-09_portfolio_holdings.csv"
df = pd.read_csv(file)

df["portfolio_date"] = pd.to_datetime(df["portfolio_date"], errors="coerce")
df["weight_pct"] = pd.to_numeric(df["weight_pct"], errors="coerce")
df["market_value_cr"] = pd.to_numeric(df["market_value_cr"], errors="coerce")
df["current_price_inr"] = pd.to_numeric(df["current_price_inr"], errors="coerce")

df = df.drop_duplicates()
df.to_csv(OUT / "portfolio_holdings_cleaned.csv", index=False)
print("Portfolio holdings cleaned:", df.shape)


# 2. Benchmark Indices
file = RAW / "1788499982615-f9647ab2-10_benchmark_indices.csv"
df = pd.read_csv(file)

df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["close_value"] = pd.to_numeric(df["close_value"], errors="coerce")

df = df[df["close_value"] > 0]
df = df.drop_duplicates()

df.to_csv(OUT / "benchmark_indices_cleaned.csv", index=False)
print("Benchmark indices cleaned:", df.shape)


# 3. Fund Master
file = RAW / "1788499983024-b042c300-01_fund_master.csv"
df = pd.read_csv(file)

df["launch_date"] = pd.to_datetime(df["launch_date"], errors="coerce")
df["expense_ratio_pct"] = pd.to_numeric(df["expense_ratio_pct"], errors="coerce")

df = df.drop_duplicates(subset=["amfi_code"])

df.to_csv(OUT / "fund_master_cleaned.csv", index=False)
print("Fund master cleaned:", df.shape)


# 4. AUM by Fund House
file = RAW / "1788499984134-b0cbf625-03_aum_by_fund_house.csv"
df = pd.read_csv(file)

df["date"] = pd.to_datetime(df["date"], errors="coerce")

for col in ["aum_lakh_crore", "aum_crore", "num_schemes"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.drop_duplicates()

df.to_csv(OUT / "aum_by_fund_house_cleaned.csv", index=False)
print("AUM cleaned:", df.shape)


# 5. Monthly SIP Inflows
file = RAW / "1788499984405-d702a6c6-04_monthly_sip_inflows.csv"
df = pd.read_csv(file)

df["month"] = pd.to_datetime(df["month"], errors="coerce")

for col in [
    "sip_inflow_crore",
    "active_sip_accounts_crore",
    "new_sip_accounts_lakh",
    "sip_aum_lakh_crore",
    "yoy_growth_pct"
]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.drop_duplicates()

df.to_csv(OUT / "monthly_sip_inflows_cleaned.csv", index=False)
print("Monthly SIP inflows cleaned:", df.shape)


# 6. Category Inflows
file = RAW / "1788499984721-4b860901-05_category_inflows.csv"
df = pd.read_csv(file)

df["month"] = pd.to_datetime(df["month"], errors="coerce")
df["net_inflow_crore"] = pd.to_numeric(
    df["net_inflow_crore"], errors="coerce"
)

df = df.drop_duplicates()

df.to_csv(OUT / "category_inflows_cleaned.csv", index=False)
print("Category inflows cleaned:", df.shape)


# 7. Industry Folio Count
file = RAW / "1788499985036-da4a0c4a-06_industry_folio_count.csv"
df = pd.read_csv(file)

df["month"] = pd.to_datetime(df["month"], errors="coerce")

for col in [
    "total_folios_crore",
    "equity_folios_crore",
    "debt_folios_crore",
    "hybrid_folios_crore",
    "others_folios_crore"
]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.drop_duplicates()

df.to_csv(OUT / "industry_folio_count_cleaned.csv", index=False)
print("Industry folio count cleaned:", df.shape)


print("\nRemaining 7 datasets cleaned successfully.")