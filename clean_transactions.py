import pandas as pd
from pathlib import Path

input_file = Path(
    "data/raw/1788499980509-304c1255-08_investor_transactions.csv"
)

output_file = Path(
    "data/processed/investor_transactions_cleaned.csv"
)

transactions = pd.read_csv(input_file)

print("Original shape:", transactions.shape)
print("\nColumns:")
print(transactions.columns.tolist())

# 1. Fix date format
date_columns = [
    col for col in transactions.columns
    if "date" in col.lower()
]

for col in date_columns:
    transactions[col] = pd.to_datetime(
        transactions[col],
        errors="coerce"
    )

# 2. Standardise transaction type
transaction_col = "transaction_type"

transactions[transaction_col] = (
    transactions[transaction_col]
    .astype(str)
    .str.strip()
    .str.upper()
)

transaction_mapping = {
    "SIP": "SIP",
    "LUMP SUM": "Lumpsum",
    "LUMPSUM": "Lumpsum",
    "REDEMPTION": "Redemption"
}

transactions[transaction_col] = (
    transactions[transaction_col]
    .map(transaction_mapping)
)

print("\nTransaction types:")
print(transactions[transaction_col].value_counts(dropna=False))

# 3. Validate amount > 0
amount_col = "amount_inr"

invalid_amounts = (
    transactions[amount_col] <= 0
).sum()

print("\nInvalid amounts:", invalid_amounts)

transactions = transactions[
    transactions[amount_col] > 0
].copy()

# 4. Check KYC status values
kyc_col = "kyc_status"

print("\nKYC status values:")
print(transactions[kyc_col].value_counts(dropna=False))

# 5. Remove exact duplicates
duplicates = transactions.duplicated().sum()

print("\nDuplicate rows:", duplicates)

transactions = transactions.drop_duplicates()

# 6. Save cleaned file
output_file.parent.mkdir(
    parents=True,
    exist_ok=True
)

transactions.to_csv(
    output_file,
    index=False
)

print("\nCleaned shape:", transactions.shape)
print("Saved:", output_file)