### 1. Project Title & Description

| Field | Value |
| --- | --- |
| Project | Sales Performance Analytics |
| Description | Retail sales analysis 2025 from 3 relational tables (Products, Sales Reps, Orders) to identify the most profitable products & regions, sales performance against target, and sales trends over the year. |
| Created by | Rafiq |
| Date | Jan 2026 |
| Data period | January – December 2025 |

### 2. Data Source

| Field | Value |
| --- | --- |
| Source | Simulated (dummy) data generated with Python (`generate_data.py`) |
| Records | 600 transactions, 10 products, 5 sales reps |
| Currency | USD |
| File | `sales.xlsx` (sheets: Products, Sales Reps, Orders, Analysis, Pivot, README) |

### 3. Data Dictionary (Column Definitions)

**Products table**

| Column | Definition |
| --- | --- |
| Product ID | Unique product code (e.g. P-01) |
| Product Name | Product name |
| Category | Product category (Electronics, Home & Living, Fashion) |
| Unit Price | Selling price per unit (USD) |
| Unit Cost | Cost price per unit (USD) |

**Sales Reps table**

| Column | Definition |
| --- | --- |
| Rep ID | Unique sales rep code (e.g. R-01) |
| Sales Rep | Sales rep name |
| Region | Assigned region |
| Hire Date | Start date |
| Monthly Target | Monthly sales target (USD) |

**Orders table (fact table)**

| Column | Definition |
| --- | --- |
| Order ID | Unique transaction code (e.g. ORD-1001) |
| Order Date | Transaction date |
| Rep ID | References the Sales Reps table |
| Product ID | References the Products table |
| Quantity | Units sold |

**Derived columns (in the Analysis sheet)**

| Column | Formula |
| --- | --- |
| Total Sales | Quantity × Unit Price |
| Profit | Quantity × (Unit Price − Unit Cost) |

### 4. KPI Definitions

| KPI | Formula / Definition |
| --- | --- |
| Total Sales | Total revenue |
| Total Profit | Total profit |
| Profit Margin | Total Profit ÷ Total Sales |
| Transactions | Number of unique Order IDs |
| Avg Order Value (AOV) | Total Sales ÷ Transactions |

### 5. Table Relationships

Excel/Sheets can't render mermaid diagrams, so write it as text in the sheet:

```
Orders (fact table)
  ├── Product ID  →  Products (Product ID)
  └── Rep ID      →  Sales Reps (Rep ID)
```

> **Explanation:** The `Orders` table is the central fact table. Each order row links to one product via **Product ID** and to one sales rep via **Rep ID**. Tables are joined using XLOOKUP (Excel/Sheets) or `merge` (Python).
>
