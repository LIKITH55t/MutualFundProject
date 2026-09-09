import pandas as pd
from pathlib import Path

input_file = Path(
    "data/raw/1788499985420-bb134abf-07_scheme_performance.csv"
)

output_file = Path(
    "data/processed/scheme_performance_cleaned.csv"
)

performance = pd.read_csv(input_file)

print("Original shape:", performance.shape)
print("\nColumns:")
print(performance.columns.tolist())

# 1. Convert numeric return/performance columns
numeric_columns = performance.select_dtypes(
    include=["number"]
).columns.tolist()

print("\nNumeric columns:")
print(numeric_columns)

for col in numeric_columns:
    performance[col] = pd.to_numeric(
        performance[col],
        errors="coerce"
    )

# 2. Check missing values created during numeric conversion
print("\nMissing values after numeric validation:")
print(performance[numeric_columns].isna().sum())

# 3. Check expense ratio range
expense_col = "expense_ratio_pct"

invalid_expense = performance[
    (performance[expense_col] < 0.1) |
    (performance[expense_col] > 2.5)
]

print(
    "\nExpense ratio anomalies:",
    len(invalid_expense)
)

# 4. Flag anomalies instead of deleting them
performance["expense_ratio_anomaly"] = (
    (performance[expense_col] < 0.1) |
    (performance[expense_col] > 2.5)
)

# 5. Check duplicate records
print(
    "\nDuplicate rows:",
    performance.duplicated().sum()
)

# 6. Save cleaned dataset
output_file.parent.mkdir(
    parents=True,
    exist_ok=True
)

performance.to_csv(
    output_file,
    index=False
)

print("\nCleaned shape:", performance.shape)
print("Saved:", output_file)