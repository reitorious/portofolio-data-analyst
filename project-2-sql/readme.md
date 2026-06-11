### 1. Project Title & Description

| Field | Value |
| --- | --- |
| Project | Food Delivery Marketplace SQL Analytics |
| Description | SQL analysis of a food-delivery marketplace across 6 relational tables (Customers, Restaurants, Drivers, Orders, Order Items, Ratings) to measure revenue trends, top restaurants, driver performance, acquisition-channel value, and customer retention — using multi-table JOINs, CTEs, and window functions. |
| Created by | Rafiq |
| Date | Feb 2026 |
| Database | SQLite (single portable file `delivery.db`) |

### 2. Data Source

| Field | Value |
| --- | --- |
| Source | Simulated (dummy) data generated with Python (`generate_data.py`) |
| Records | 200 customers, 40 restaurants, 30 drivers, ~3,000 orders, ~7,500 order items, ~1,800 ratings |
| Currency | USD |
| Engine | SQLite 3 (portable to PostgreSQL/MySQL with minor syntax changes) |

### 3. Data Dictionary (Column Definitions)

**customers table**

| Column | Definition |
| --- | --- |
| customer_id | Primary key, unique customer ID |
| customer_name | Customer name |
| city | Customer's city |
| signup_date | Signup date (YYYY-MM-DD) |
| channel | Acquisition channel (Organic, Paid Ads, Referral, Social Media) |

**restaurants table**

| Column | Definition |
| --- | --- |
| restaurant_id | Primary key, unique restaurant ID |
| restaurant_name | Restaurant name |
| city | Restaurant's city |
| cuisine | Cuisine type (Indonesian, Japanese, Western, etc.) |
| commission_rate | Platform commission rate (0.10–0.25) |

**drivers table**

| Column | Definition |
| --- | --- |
| driver_id | Primary key, unique driver ID |
| driver_name | Driver name |
| vehicle_type | Vehicle used (Motorcycle, Car, Bicycle) |
| city | Driver's operating city |
| join_date | Date the driver joined |

**orders table (fact)**

| Column | Definition |
| --- | --- |
| order_id | Primary key, unique order ID |
| customer_id | References the customers table |
| restaurant_id | References the restaurants table |
| driver_id | References the drivers table |
| order_date | Transaction date |
| order_status | Completed, Cancelled, or Refunded |
| delivery_minutes | Delivery time in minutes (null if not completed) |

**order_items table**

| Column | Definition |
| --- | --- |
| order_item_id | Primary key, unique line-item ID |
| order_id | References the orders table |
| item_name | Menu item name |
| category | Item category (= restaurant cuisine) |
| quantity | Number of units ordered |
| unit_price | Price per unit (USD) |

**ratings table**

| Column | Definition |
| --- | --- |
| rating_id | Primary key, unique rating ID |
| order_id | References the orders table |
| food_rating | Food rating 1–5 |
| delivery_rating | Delivery rating 1–5 |
| created_at | When the rating was given |

### 4. KPI Definitions

| KPI | Formula / Definition |
| --- | --- |
| Total Revenue | Σ (quantity × unit_price) for Completed orders |
| Completed Orders | Number of orders with status Completed |
| AOV (Avg Order Value) | Total Revenue ÷ number of Completed orders |
| Avg Delivery Time | AVG(delivery_minutes) for Completed orders |
| Cancellation Rate | (Cancelled + Refunded) ÷ all orders |
| Repeat Rate | Customers with ≥2 orders ÷ customers with ≥1 order |