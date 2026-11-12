import pandas as pd
from pathlib import Path

# Find the Excel file automatically
raw_path = next(Path("data/raw").glob("*.xlsx"))
print("Reading file:", raw_path)

# Load BOTH sheets and combine them
xls = pd.ExcelFile(raw_path)
print("Sheets:", xls.sheet_names)

frames = [pd.read_excel(raw_path, sheet_name=s) for s in xls.sheet_names]
df = pd.concat(frames, ignore_index=True)

print("\nShape:", df.shape)
print("\nColumns:", list(df.columns))
print("\nDtypes:\n", df.dtypes)

# Date range
date_col = [c for c in df.columns if "date" in c.lower()][0]
df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
print("\nDate range:", df[date_col].min(), "->", df[date_col].max())
print("Invalid dates:", df[date_col].isna().sum())

# Nulls and first rows
print("\nNull counts:\n", df.isna().sum())
print("\nFirst rows:\n", df.head())