import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Sales Performance Dashboard", layout="wide")

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

@st.cache_data
def load_data():
    orders = pd.read_csv("data/orders.csv", parse_dates=["Order Date"])
    products = pd.read_csv("data/products.csv")
    reps = pd.read_csv("data/sales_reps.csv")

    # Join the three tables into one analysis table
    df = (orders
          .merge(products, on="Product ID", how="left")
          .merge(reps, on="Rep ID", how="left"))

    df["Total Sales"] = df["Quantity"] * df["Unit Price"]
    df["Profit"] = df["Quantity"] * (df["Unit Price"] - df["Unit Cost"])
    df["Month"] = df["Order Date"].dt.to_period("M").astype(str)
    return df, reps

df, reps = load_data()

st.title("📊 Sales Performance Dashboard")
st.caption("Retail sales analysis 2025 — built from 3 related tables")

# === Sidebar filters ===
st.sidebar.header("Filters")
region = st.sidebar.multiselect("Region", sorted(df["Region"].unique()),
                                default=sorted(df["Region"].unique()))
category = st.sidebar.multiselect("Category", sorted(df["Category"].unique()),
                                  default=sorted(df["Category"].unique()))
data = df[df["Region"].isin(region) & df["Category"].isin(category)]

# === KPI row ===
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total Sales", f"${data['Total Sales'].sum():,.0f}")
c2.metric("Total Profit", f"${data['Profit'].sum():,.0f}")
margin = data["Profit"].sum() / max(data["Total Sales"].sum(), 1) * 100
c3.metric("Profit Margin", f"{margin:.1f}%")
c4.metric("Transactions", f"{data['Order ID'].nunique():,}")
aov = data["Total Sales"].sum() / max(data["Order ID"].nunique(), 1)
c5.metric("Avg Order Value", f"${aov:,.0f}")

st.divider()

# === Monthly trend ===
trend = data.groupby("Month", as_index=False)["Total Sales"].sum()
st.plotly_chart(px.line(trend, x="Month", y="Total Sales", markers=True,
                        title="Monthly Sales Trend"), use_container_width=True)

k1, k2 = st.columns(2)
by_region = (data.groupby("Region", as_index=False)["Total Sales"].sum()
                 .sort_values("Total Sales"))
k1.plotly_chart(px.bar(by_region, x="Total Sales", y="Region", orientation="h",
                       title="Sales by Region"), use_container_width=True)
by_cat = data.groupby("Category", as_index=False)["Profit"].sum()
k2.plotly_chart(px.pie(by_cat, names="Category", values="Profit",
                       title="Profit Contribution by Category"),
                use_container_width=True)

# === Sales vs target per rep ===
actual = data.groupby("Sales Rep", as_index=False)["Total Sales"].sum()
target = reps.copy()
target["Annual Target"] = target["Monthly Target"] * 12
perf = actual.merge(target[["Sales Rep", "Annual Target"]], on="Sales Rep", how="left")
perf = perf.sort_values("Total Sales", ascending=False)

g1, g2 = st.columns(2)
fig_rep = px.bar(perf, x="Sales Rep", y=["Total Sales", "Annual Target"],
                 barmode="group", title="Sales vs Target by Rep")
g1.plotly_chart(fig_rep, use_container_width=True)

top_prod = (data.groupby("Product Name", as_index=False)["Total Sales"].sum()
                .sort_values("Total Sales", ascending=False).head(10))
g2.plotly_chart(px.bar(top_prod, x="Total Sales", y="Product Name",
                       orientation="h", title="Top 10 Products"),
                use_container_width=True)

st.divider()
st.subheader("💡 Insights & Recommendations")

# Derive key facts directly from the filtered data
top_region = by_region.sort_values("Total Sales", ascending=False).iloc[0]
top_cat = by_cat.sort_values("Profit", ascending=False).iloc[0]
peak = trend.sort_values("Total Sales", ascending=False).iloc[0]
low = trend.sort_values("Total Sales").iloc[0]
peak_month = pd.to_datetime(str(peak['Month'])).strftime('%b %Y')
low_month = pd.to_datetime(str(low['Month'])).strftime('%b %Y')
below_target = perf[perf["Total Sales"] < 0.7 * perf["Annual Target"]]
margin = data["Profit"].sum() / max(data["Total Sales"].sum(), 1) * 100

st.markdown(rf"""
- **Top region:** {top_region['Region']} leads with ${top_region['Total Sales']:,.0f} in sales.
  _Recommendation:_ concentrate stock and promotions in {top_region['Region']} and replicate its playbook in weaker regions.
- **Most profitable category:** {top_cat['Category']} drives the highest profit (${top_cat['Profit']:,.0f}).
  _Recommendation:_ expand the {top_cat['Category']} range and bundle it with lower-margin items.
- **Seasonality:** sales peak in {peak_month} (\${peak['Total Sales']:,.0f}) and dip in {low_month} (\${low['Total Sales']:,.0f}).
  _Recommendation:_ plan campaigns ahead of peak months and run retention offers during the dip.
- **Sales reps:** {len(below_target)} of {len(perf)} reps are below 70% of their annual target.
  _Recommendation:_ pair them with top performers for coaching and review territory allocation.
- **Overall profit margin:** {margin:.1f}%.
""")

st.subheader("Detailed Data (joined)")
st.dataframe(data, use_container_width=True)