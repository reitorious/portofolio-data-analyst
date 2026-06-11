# dashboard.py — Streamlit dashboard powered by SQL (SQLite)
import sqlite3
import pandas as pd
import plotly.express as px
import streamlit as st
from pathlib import Path

BASE_DIR = Path(__file__).parent
DB = BASE_DIR / "delivery.db" 

st.set_page_config(page_title="Food Delivery SQL Dashboard", layout="wide")

# Hide Streamlit toolbar (Deploy button), main menu, and footer for a clean look
hide_ui = """
<style>
.stDeployButton {display: none;}
[data-testid="stToolbar"] {visibility: hidden;}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_ui, unsafe_allow_html=True)

# Run any SQL string against the database and return a DataFrame
@st.cache_data
def run_sql(query, params=None):
    conn = sqlite3.connect(DB)
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

st.title("🍔 Food Delivery — SQL Analytics Dashboard")
st.caption("Powered by SQL queries on a 6-table SQLite database")

# === Sidebar filter: city ===
cities = run_sql("SELECT DISTINCT city FROM restaurants ORDER BY city")["city"].tolist()
city = st.sidebar.multiselect("City", cities, default=cities)
# Build a safe placeholder list, e.g. (?,?,?) — values are passed via params
city_filter = "(" + ",".join("?" * len(city)) + ")" if city else "(NULL)"

# === KPI row (all computed in SQL) ===
kpi = run_sql(f"""
    SELECT
        ROUND(SUM(oi.quantity * oi.unit_price), 0)           AS revenue,
        COUNT(DISTINCT o.order_id)                           AS orders,
        ROUND(SUM(oi.quantity * oi.unit_price) /
              COUNT(DISTINCT o.order_id), 2)                 AS aov,
        ROUND(AVG(o.delivery_minutes), 1)                    AS avg_delivery
    FROM orders o
    JOIN order_items oi ON oi.order_id = o.order_id
    JOIN restaurants r  ON r.restaurant_id = o.restaurant_id
    WHERE o.order_status = 'Completed' AND r.city IN {city_filter}
""", params=city)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Revenue", f"${kpi['revenue'][0]:,.0f}")
c2.metric("Completed Orders", f"{kpi['orders'][0]:,}")
c3.metric("Avg Order Value", f"${kpi['aov'][0]:,.2f}")
c4.metric("Avg Delivery (min)", f"{kpi['avg_delivery'][0]:.1f}")

st.divider()

# === Monthly revenue trend (SQL aggregation) ===
monthly = run_sql(f"""
    SELECT strftime('%Y-%m', o.order_date) AS month,
           ROUND(SUM(oi.quantity * oi.unit_price), 2) AS revenue
    FROM orders o
    JOIN order_items oi ON oi.order_id = o.order_id
    JOIN restaurants r  ON r.restaurant_id = o.restaurant_id
    WHERE o.order_status = 'Completed' AND r.city IN {city_filter}
    GROUP BY month ORDER BY month
""", params=city)
st.plotly_chart(px.line(monthly, x="month", y="revenue", markers=True,
                        title="Monthly Revenue Trend"), use_container_width=True)

g1, g2 = st.columns(2)

# Top 10 restaurants by revenue
top_resto = run_sql(f"""
    SELECT r.restaurant_name, ROUND(SUM(oi.quantity * oi.unit_price), 2) AS revenue
    FROM restaurants r
    JOIN orders o       ON o.restaurant_id = r.restaurant_id AND o.order_status = 'Completed'
    JOIN order_items oi ON oi.order_id = o.order_id
    WHERE r.city IN {city_filter}
    GROUP BY r.restaurant_id ORDER BY revenue DESC LIMIT 10
""", params=city)
g1.plotly_chart(px.bar(top_resto, x="revenue", y="restaurant_name", orientation="h",
                       title="Top 10 Restaurants by Revenue"), use_container_width=True)

# Revenue by food category
by_cat = run_sql(f"""
    SELECT oi.category, ROUND(SUM(oi.quantity * oi.unit_price), 2) AS revenue
    FROM order_items oi
    JOIN orders o      ON o.order_id = oi.order_id AND o.order_status = 'Completed'
    JOIN restaurants r ON r.restaurant_id = o.restaurant_id
    WHERE r.city IN {city_filter}
    GROUP BY oi.category ORDER BY revenue DESC
""", params=city)
g2.plotly_chart(px.pie(by_cat, names="category", values="revenue",
                       title="Revenue by Category"), use_container_width=True)

# === Revenue by acquisition channel ===
by_channel = run_sql(f"""
    SELECT c.channel, ROUND(SUM(oi.quantity * oi.unit_price), 2) AS revenue
    FROM customers c
    JOIN orders o       ON o.customer_id = c.customer_id AND o.order_status = 'Completed'
    JOIN order_items oi ON oi.order_id = o.order_id
    JOIN restaurants r  ON r.restaurant_id = o.restaurant_id
    WHERE r.city IN {city_filter}
    GROUP BY c.channel ORDER BY revenue DESC
""", params=city)
st.plotly_chart(px.bar(by_channel, x="channel", y="revenue",
                       title="Revenue by Acquisition Channel"), use_container_width=True)

st.subheader("Top 3 Restaurants per City")
top_city = run_sql("""
    WITH resto_rev AS (
        SELECT r.city, r.restaurant_name,
               SUM(oi.quantity * oi.unit_price) AS revenue
        FROM restaurants r
        JOIN orders o       ON o.restaurant_id = r.restaurant_id AND o.order_status = 'Completed'
        JOIN order_items oi ON oi.order_id = o.order_id
        GROUP BY r.restaurant_id
    )
    SELECT city, restaurant_name, ROUND(revenue, 2) AS revenue
    FROM (
        SELECT city, restaurant_name, revenue,
               ROW_NUMBER() OVER (PARTITION BY city ORDER BY revenue DESC) AS rnk
        FROM resto_rev
    ) WHERE rnk <= 3 ORDER BY city, revenue DESC
""")
st.dataframe(top_city, use_container_width=True)

st.divider()
st.subheader("💡 Insights & Recommendations")

# Channel value (revenue per acquired customer), computed in SQL
channel_val = run_sql("""
    SELECT c.channel,
           ROUND(SUM(oi.quantity * oi.unit_price) /
                 COUNT(DISTINCT c.customer_id), 2) AS revenue_per_customer
    FROM customers c
    JOIN orders o       ON o.customer_id = c.customer_id AND o.order_status = 'Completed'
    JOIN order_items oi ON oi.order_id = o.order_id
    GROUP BY c.channel ORDER BY revenue_per_customer DESC
""")

peak = monthly.sort_values("revenue", ascending=False).iloc[0]
low = monthly.sort_values("revenue").iloc[0]
best_resto = top_resto.iloc[0]
best_cat = by_cat.iloc[0]
best_channel = channel_val.iloc[0]

st.markdown(f"""
- **Revenue seasonality:** highest in {peak['month']} (${peak['revenue']:,.0f}), lowest in {low['month']} (${low['revenue']:,.0f}).
  _Recommendation:_ schedule marketing pushes before peak months and retention offers during slow months.
- **Restaurant concentration:** {best_resto['restaurant_name']} is the top earner (${best_resto['revenue']:,.0f}).
  _Recommendation:_ secure exclusive deals with top restaurants and coach mid-tier partners.
- **Category demand:** {best_cat['category']} generates the most revenue (${best_cat['revenue']:,.0f}).
  _Recommendation:_ feature {best_cat['category']} on the homepage and grow its restaurant supply.
- **Best acquisition channel:** {best_channel['channel']} delivers the highest revenue per customer (${best_channel['revenue_per_customer']:,.2f}).
  _Recommendation:_ shift more budget toward {best_channel['channel']} and audit low-value channels.
- **Operations:** average delivery time is {kpi['avg_delivery'][0]:.1f} min.
  _Recommendation:_ investigate cities or drivers above this benchmark to protect delivery ratings.
""")
