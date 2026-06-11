# clean_data.py — part 1: inspection
import pandas as pd
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).parent    

df = pd.read_csv(BASE_DIR / "AB_NYC_2019.csv")

print("Data shape:", df.shape)              # (rows, columns)
print("\n--- Data types & non-null ---")
print(df.info())
print("\n--- Missing values per column ---")
print(df.isnull().sum())
print("\n--- Number of duplicate rows ---")
print(df.duplicated().sum())
print("\n--- Numeric column statistics ---")
print(df.describe())
print("\n--- Check odd prices (0 or extreme) ---")
print("Price = 0:", (df['price'] == 0).sum())
print("Price > 1000:", (df['price'] > 1000).sum())

# --- Capture data-quality metrics BEFORE cleaning, so we can prove the impact later ---
rows_before = len(df)                        # total rows in the raw data
nulls_before = int(df.isnull().sum().sum())  # total missing values across all columns
dupes_before = int(df.duplicated().sum())    # number of exact duplicate rows

# Issue #7 — drop exact duplicate rows to prevent double-counting in any analysis
df = df.drop_duplicates()

# name & host_name missing -> fill with "Unknown" (keep the row)
df['name'] = df['name'].fillna("Unknown")
df['host_name'] = df['host_name'].fillna("Unknown")

# reviews_per_month missing = listing has no reviews yet -> 0
df['reviews_per_month'] = df['reviews_per_month'].fillna(0)

# last_review is still text -> convert to a real datetime
df['last_review'] = pd.to_datetime(df['last_review'], errors='coerce')

# price 0 is impossible for an active listing -> remove
df = df[df['price'] > 0]

# IQR rule: values outside [Q1 - 1.5*IQR, Q3 + 1.5*IQR] are outliers
Q1 = df['price'].quantile(0.25)
Q3 = df['price'].quantile(0.75)
IQR = Q3 - Q1
upper_cap = Q3 + 1.5 * IQR

# 'cap' (don't drop) to avoid losing too many rows
df['price'] = np.where(df['price'] > upper_cap, upper_cap, df['price'])
print("Upper price cap:", round(upper_cap, 2))

# minimum_nights > 365 (more than a year) is unrealistic -> cap at 365
df['minimum_nights'] = np.where(df['minimum_nights'] > 365, 365, df['minimum_nights'])

# strip leading/trailing whitespace
for col in ['name', 'neighbourhood_group', 'neighbourhood', 'room_type']:
    df[col] = df[col].astype(str).str.strip()

# standardize borough capitalization (in case of casing typos)
df['neighbourhood_group'] = df['neighbourhood_group'].str.title()

# flag listings that have never been reviewed
df['has_reviews'] = df['number_of_reviews'] > 0

# price category to make filtering easy
df['price_category'] = pd.cut(
    df['price'],
    bins=[0, 75, 150, 300, float('inf')],
    labels=['Budget', 'Mid', 'High', 'Luxury']
)

# short summary of changes
rows_after = len(df)
nulls_after = int(df.isnull().sum().sum())

print("\n===== CLEANING REPORT =====")
print(f"Rows   : {rows_before} -> {rows_after}  (dropped {rows_before - rows_after})")
print(f"Nulls  : {nulls_before} -> {nulls_after}")
print(f"Duplicates dropped: {dupes_before}")

# save to a NEW file (never overwrite the raw data!)
df.to_csv(BASE_DIR / "airbnb_clean.csv", index=False)
print("\nSaved to airbnb_clean.csv ✅")
