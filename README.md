# 📊 Data Analyst Portfolio

A collection of **3 end-to-end data analyst projects**, each in its own folder with a self-contained dataset, code, and an interactive **Streamlit** dashboard. Together they cover the full analyst workflow: spreadsheets & relational joins (Excel/Python), database querying (SQL), and real-world data cleaning.

## 🔗 Live Demos

| Project | Live Demo | Code |
| --- | --- | --- |
| **Sales Performance Analytics** | [Open app](https://xlx-sales.streamlit.app/) | `project-1-xlx/` |
| **SQL Analytics — Food Delivery** | [Open app](https://sql-food-delivery.streamlit.app/) | `project-2-sql/` |
| **Data Cleaning — NYC Airbnb** | [Open app](https://data-cleaning-air.streamlit.app/) | `project-3-data_cleaning/` |

## 📂 Repository Structure

    portofolio-data-analyst/
    ├── project-1-xlx/             # Project 01 — Sales Performance Analytics
    ├── project-2-sql/             # Project 04 — SQL Analytics (Food Delivery)
    ├── project-3-data_cleaning/   # Project 05 — Data Cleaning (NYC Airbnb)
    └── README.md

## 🗂️ Projects at a Glance

| Folder | Project | What it demonstrates |
| --- | --- | --- |
| `project-1-xlx/` | Sales Performance Analytics | Relational joins (3 tables), Excel pivots & a Python dashboard, sales/profit KPIs |
| `project-2-sql/` | SQL Analytics — Food Delivery | A 6-table SQLite database with multi-table JOINs, CTEs & window functions |
| `project-3-data_cleaning/` | Data Cleaning — NYC Airbnb | Cleaning real, messy public data (missing values, outliers, duplicates) |

---

## 📁 project-1-xlx/ — Sales Performance Analytics

**Purpose:** Analyze retail sales from 3 related tables to find the most profitable products & regions, sales-rep performance vs target, and yearly trends.

![Sales dashboard demo](project-1-xlx/screenshots/demo.gif)

| File / Folder | Purpose |
| --- | --- |
| `generate_data.py` | Generates the dataset (`sales.xlsx` + CSV exports) |
| `data/` | `sales.xlsx` (sheets: Products, Sales Reps, Orders) + `products.csv`, `sales_reps.csv`, `orders.csv` |
| `dashboard.py` | Streamlit dashboard that joins the 3 tables and shows KPIs & charts |
| `requirements.txt` | streamlit, pandas, plotly, openpyxl |

## 📁 project-2-sql/ — SQL Analytics: Food Delivery

**Purpose:** Demonstrate SQL skills on a food-delivery marketplace database with 6 relational tables, answering real business questions via JOINs, CTEs, and window functions.

![SQL dashboard demo](project-2-sql/screenshots/demo.gif)

| File / Folder | Purpose |
| --- | --- |
| `generate_data.py` | Builds `delivery.db` (6 tables) and fills it with realistic dummy data |
| `delivery.db` | The SQLite database (single portable file) read by the dashboard |
| `queries/` | Analytical `.sql` files (monthly revenue, top restaurants, driver performance, cohort retention, etc.) |
| `dashboard.py` | Streamlit dashboard where every KPI & chart is computed by a SQL query |
| `requirements.txt` | streamlit, pandas, plotly |

## 📁 project-3-data_cleaning/ — Data Cleaning: NYC Airbnb

**Purpose:** Take the real, messy NYC Airbnb Open Data (~48.9k rows) and turn it into a clean, analysis-ready dataset with a documented, reproducible pipeline.

![Data cleaning dashboard demo](project-3-data_cleaning/screenshots/demo.gif)

| File / Folder | Purpose |
| --- | --- |
| `AB_NYC_2019.csv` | Raw, messy source data from Kaggle (never edited directly) |
| `clean_data.py` | Cleaning pipeline: missing values, invalid prices, outliers, types, duplicates & text |
| `airbnb_clean.csv` | The cleaned output (produced by `clean_data.py`) read by the dashboard |
| `dashboard.py` | Streamlit dashboard exploring the cleaned data (prices, room types, map) |
| `requirements.txt` | streamlit, pandas, plotly |

---

## ▶️ How to Run Locally

    # 1. clone the repo
    git clone https://github.com/reitorious/portofolio-data-analyst.git
    cd portofolio-data-analyst

    # 2. go into any project folder
    cd project-1-xlx

    # 3. install dependencies & run the dashboard
    pip install -r requirements.txt
    streamlit run dashboard.py

## 🧰 Tech Stack

**Python** (pandas, plotly, streamlit) · **SQL** (SQLite) · **Excel & Google Sheets**

## 👤 Author

**Rafiq** — June 2026

