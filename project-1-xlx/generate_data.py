import pandas as pd
import numpy as np

np.random.seed(42)  # keep random results consistent

# === Table 1: Products (master) ===
products = [
    ("P-01", "Headset", "Electronics", 75, 45),
    ("P-02", "Mouse", "Electronics", 25, 12),
    ("P-03", "Keyboard", "Electronics", 40, 22),
    ("P-04", "Webcam", "Electronics", 60, 35),
    ("P-05", "Blender", "Home & Living", 50, 30),
    ("P-06", "Iron", "Home & Living", 35, 20),
    ("P-07", "Fan", "Home & Living", 45, 25),
    ("P-08", "T-Shirt", "Fashion", 20, 8),
    ("P-09", "Pants", "Fashion", 40, 18),
    ("P-10", "Shoes", "Fashion", 75, 40),
]
products_df = pd.DataFrame(products, columns=[
    "Product ID", "Product Name", "Category", "Unit Price", "Unit Cost"])

# === Table 2: Sales Reps (master) ===
reps = [
    ("R-01", "John", "New York", "2022-03-15", 15000),
    ("R-02", "Mike", "Los Angeles", "2021-07-01", 18000),
    ("R-03", "Sarah", "Chicago", "2023-01-10", 12000),
    ("R-04", "David", "Houston", "2020-11-20", 16000),
    ("R-05", "Emma", "Miami", "2022-09-05", 14000),
]
reps_df = pd.DataFrame(reps, columns=[
    "Rep ID", "Sales Rep", "Region", "Hire Date", "Monthly Target"])

# === Table 3: Orders (fact) ===
n = 600
dates = pd.to_datetime("2025-01-01") + pd.to_timedelta(
    np.random.randint(0, 365, size=n), unit="D")
orders = []
for i in range(n):
    orders.append({
        "Order ID": f"ORD-{1000 + i}",
        "Order Date": dates[i].date(),
        "Rep ID": np.random.choice(reps_df["Rep ID"]),
        "Product ID": np.random.choice(products_df["Product ID"]),
        "Quantity": int(np.random.randint(1, 11)),
    })
orders_df = pd.DataFrame(orders).sort_values("Order Date").reset_index(drop=True)

# === Save all 3 tables into ONE Excel file (multiple sheets) + CSVs ===
with pd.ExcelWriter("data/sales.xlsx") as writer:
    products_df.to_excel(writer, sheet_name="Products", index=False)
    reps_df.to_excel(writer, sheet_name="Sales Reps", index=False)
    orders_df.to_excel(writer, sheet_name="Orders", index=False)

products_df.to_csv("data/products.csv", index=False)
reps_df.to_csv("data/sales_reps.csv", index=False)
orders_df.to_csv("data/orders.csv", index=False)
print("Created:", products_df.shape, reps_df.shape, orders_df.shape)