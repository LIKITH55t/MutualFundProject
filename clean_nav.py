import pandas as pd
from pathlib import Path

# Input and output paths
input_file = Path(
    "data/raw/1788499983331-4389156d-02_nav_history.csv"
)

output_file = Path(
    "data/processed/nav_history_cleaned.csv"
)

# Load data
nav = pd.read_csv(input_file)

print("Original shape:", nav.shape)

# 1. Parse dates
nav["date"] = pd.to_datetime(
    nav["date"],
    errors="coerce"
)

# Check invalid dates
print("Invalid dates:", nav["date"].isna().sum())

# 2. Sort by AMFI code and date
nav = nav.sort_values(
    ["amfi_code", "date"]
).reset_index(drop=True)

# 3. Remove duplicate records
duplicates = nav.duplicated(
    subset=["amfi_code", "date"]
).sum()

print("Duplicates found:", duplicates)

nav = nav.drop_duplicates(
    subset=["amfi_code", "date"],
    keep="first"
)

# 4. Validate NAV > 0
invalid_nav = (nav["nav"] <= 0).sum()

print("Invalid NAV values:", invalid_nav)

# Remove invalid NAV values
nav = nav[nav["nav"] > 0].copy()

# 5. Forward-fill missing NAV within each scheme
missing_before = nav["nav"].isna().sum()

nav["nav"] = (
    nav.groupby("amfi_code")["nav"]
    .ffill()
)

missing_after = nav["nav"].isna().sum()

print("Missing NAV before fill:", missing_before)
print("Missing NAV after fill:", missing_after)

# 6. Save cleaned dataset
output_file.parent.mkdir(
    parents=True,
    exist_ok=True
)

nav.to_csv(
    output_file,
    index=False
)

print("\nCleaned shape:", nav.shape)
print("Saved:", output_file)