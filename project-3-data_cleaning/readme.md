### 1. Project Title & Description

| Field | Value |
| --- | --- |
| Project | NYC Airbnb Data Cleaning |
| Description | End-to-end cleaning of the real-world NYC Airbnb Open Data (~48.9k listings): handling missing values, removing invalid prices, capping outliers with the IQR method, fixing data types, dropping duplicates, and standardizing text — producing an analysis-ready dataset with a documented, reproducible pipeline. |
| Created by | Rafiq |
| Date | May 2026 |
| Tools | Python (pandas, numpy) |

### 2. Data Source

| Field | Value |
| --- | --- |
| Source | Kaggle — New York City Airbnb Open Data (dgomonov), file `AB_NYC_2019.csv` |
| Type | Real, public, raw data (not generated) |
| Records | ~48,895 rows × 16 columns (raw) |

### 3. Cleaning Steps Summary

| Step | Action | Reason |
| --- | --- | --- |
| Duplicates | Dropped exact duplicate rows | Prevent double-counting |
| Missing text | Filled `name` / `host_name` with "Unknown" | Keep otherwise-valid rows |
| Missing reviews | Filled `reviews_per_month` with 0 | Missing means no reviews yet |
| Invalid price | Removed rows where price = 0 | A paid listing cannot be free |
| Price outliers | Capped using IQR upper bound | Avoid skewing averages |
| Nights outliers | Capped `minimum_nights` at 365 | Over a year is unrealistic |
| Wrong type | Converted `last_review` to datetime | Enable time-based analysis |
| Inconsistent text | Trimmed & standardized casing | Reliable grouping/filtering |

### 4. Before vs After

| Metric | Before | After |
| --- | --- | --- |
| Rows | 48,895 | 48,884 |
| Total missing values | 20,141 | 10,051 |
| Duplicate rows | 0 | 0 |
| Price = 0 | 11 | 0 |

### 5. Live Demo

[Open dashboard project-03 data cleaning](https://data-cleaning-air.streamlit.app/)

[Before data cleaning](https://data-cleaning-air.streamlit.app/](https://drive.google.com/file/d/1nc2HxOu5QfLbzgWng5jvxMlz_LUTl8ny/view?usp=sharing/))

[After data cleaning](https://data-cleaning-air.streamlit.app/](https://drive.google.com/file/d/1UqDDUOAkhe716cf4lePoVI0xfCAN5wGc/view?usp=drive_link/))
