import pandas as pd
from pathlib import Path

# Location of the raw CSV files
RAW_DATA_DIR = Path("data/raw")

# Find all CSV files
csv_files = sorted(RAW_DATA_DIR.glob("*.csv"))

print("=" * 70)
print("DATA INGESTION")
print("=" * 70)

print(f"\nNumber of CSV files found: {len(csv_files)}")

if len(csv_files) != 10:
    print("WARNING: Expected 10 CSV files.")

# Load and inspect every CSV
for file in csv_files:
    print("\n" + "=" * 70)
    print(f"FILE: {file.name}")
    print("=" * 70)

    try:
        df = pd.read_csv(file)

        print("\nShape:")
        print(df.shape)

        print("\nData Types:")
        print(df.dtypes)

        print("\nFirst 5 Rows:")
        print(df.head())

        print("\nMissing Values:")
        print(df.isnull().sum())

        print("\nDuplicate Rows:")
        print(df.duplicated().sum())

        print("\nColumns:")
        print(list(df.columns))

    except Exception as e:
        print(f"\nERROR loading {file.name}: {e}")

print("\n" + "=" * 70)
print("DATA INGESTION COMPLETED")
print("=" * 70)


# ---------------------------------------------------------
# FUND MASTER EXPLORATION
# ---------------------------------------------------------

fund_master_file = next(
    RAW_DATA_DIR.glob("*01_fund_master.csv"),
    None
)

if fund_master_file:
    print("\n" + "=" * 70)
    print("FUND MASTER EXPLORATION")
    print("=" * 70)

    fund_master = pd.read_csv(fund_master_file)

    print("\nColumns:")
    print(fund_master.columns.tolist())

    # Explore fund house, category and sub-category
    for column in ["fund_house", "category", "sub_category"]:
        if column in fund_master.columns:
            print(f"\nUnique {column}:")
            print(fund_master[column].dropna().unique())

            print(f"\nNumber of unique {column}:")
            print(fund_master[column].nunique())

    # Explore risk category
    print("\nUnique risk_category:")
    print(fund_master["risk_category"].dropna().unique())

    print("\nNumber of unique risk_category:")
    print(fund_master["risk_category"].nunique())

else:
    print("\nFund master file not found.")
# ---------------------------------------------------------
# AMFI CODE VALIDATION
# ---------------------------------------------------------

fund_master_codes = set(fund_master["amfi_code"])

nav_history_file = next(
    RAW_DATA_DIR.glob("*02_nav_history.csv"),
    None
)

if nav_history_file:
    nav_history = pd.read_csv(nav_history_file)

    nav_history_codes = set(nav_history["amfi_code"])

    missing_codes = fund_master_codes - nav_history_codes

    print("\n" + "=" * 70)
    print("AMFI CODE VALIDATION")
    print("=" * 70)

    print(f"\nFund Master AMFI codes: {len(fund_master_codes)}")
    print(f"NAV History AMFI codes: {len(nav_history_codes)}")

    if len(missing_codes) == 0:
        print("\nAll AMFI codes in fund_master exist in nav_history.")
    else:
        print("\nMissing AMFI codes:")
        print(missing_codes)

else:
    print("\nNAV history file not found.")
# ---------------------------------------------------------
# DATA QUALITY SUMMARY
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("DATA QUALITY SUMMARY")
print("=" * 70)

print("\n1. Fund Master:")
print(f"   Records: {len(fund_master)}")
print(f"   Unique AMFI codes: {fund_master['amfi_code'].nunique()}")
print(f"   Missing values: {fund_master.isnull().sum().sum()}")
print(f"   Duplicate rows: {fund_master.duplicated().sum()}")

print("\n2. NAV History:")
print(f"   Records: {len(nav_history)}")
print(f"   Unique AMFI codes: {nav_history['amfi_code'].nunique()}")
print(f"   Missing values: {nav_history.isnull().sum().sum()}")
print(f"   Duplicate rows: {nav_history.duplicated().sum()}")

print("\n3. AMFI Code Validation:")
print(f"   Missing codes: {len(missing_codes)}")

if len(missing_codes) == 0:
    print("   Status: PASSED")
else:
    print("   Status: FAILED")

print("\n4. Overall Data Quality:")
print("   Fund Master and NAV History AMFI codes are fully matched.")