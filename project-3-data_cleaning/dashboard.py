# dashboard.py — NYC Airbnb cleaned-data dashboard
import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="NYC Airbnb Dashboard", layout="wide")

# --- hide Streamlit's top-right toolbar / deploy button ---
hide_ui = """
    <style>
    .stDeployButton {display:none;}
    [data-testid="stToolbar"] {visibility:hidden;}
    #MainMenu {visibility:hidden;}
    footer {visibility:hidden;}
    </style>
"""
st.markdown(hide_ui, unsafe_allow_html=True)

@st.cache_data
def load_data():
    return pd.read_csv("airbnb_clean.csv", parse_dates=["last_review"])

df = load_data()

st.title("🏙️ NYC Airbnb — Market Dashboard")
st.caption("Built on the cleaned AB_NYC_2019 dataset (analysis-ready).")

# --- Sidebar filters ---
st.sidebar.header("Filters")
boroughs = sorted(df["neighbourhood_group"].dropna().unique())
rooms = sorted(df["room_type"].dropna().unique())
sel_boroughs = st.sidebar.multiselect("Borough", boroughs, default=boroughs)
sel_rooms = st.sidebar.multiselect("Room type", rooms, default=rooms)

data = df[df["neighbourhood_group"].isin(sel_boroughs) & df["room_type"].isin(sel_rooms)]

# --- KPI cards ---
c1, c2, c3, c4 = st.columns(4)
c1.metric("Listings", f"{len(data):,}")
c2.metric("Median price / night", f"${data['price'].median():,.0f}")
c3.metric("Avg availability", f"{data['availability_365'].mean():.0f} days")
no_review_pct = (data['number_of_reviews'] == 0).mean() * 100
c4.metric("Listings w/o reviews", f"{no_review_pct:.1f}%")

st.divider()

# --- Charts ---
g1, g2 = st.columns(2)
with g1:
    st.subheader("Average price by borough")
    by_boro = (data.groupby("neighbourhood_group", as_index=False)["price"]
                   .mean().sort_values("price", ascending=False))
    fig = px.bar(by_boro, x="neighbourhood_group", y="price", text_auto=".0f")
    fig.update_layout(xaxis_title="", yaxis_title="Avg price ($)")
    st.plotly_chart(fig, use_container_width=True)
with g2:
    st.subheader("Listings by room type")
    by_room = data["room_type"].value_counts().reset_index()
    by_room.columns = ["room_type", "count"]
    fig = px.pie(by_room, names="room_type", values="count", hole=0.4)
    st.plotly_chart(fig, use_container_width=True)

g3, g4 = st.columns(2)
with g3:
    st.subheader("Top 10 neighbourhoods by listings")
    top_nb = data["neighbourhood"].value_counts().head(10).reset_index()
    top_nb.columns = ["neighbourhood", "count"]
    fig = px.bar(top_nb.sort_values("count"), x="count", y="neighbourhood", orientation="h")
    fig.update_layout(xaxis_title="Listings", yaxis_title="")
    st.plotly_chart(fig, use_container_width=True)
with g4:
    st.subheader("Listings by price category")
    by_cat = (data["price_category"].value_counts()
                  .reindex(["Budget", "Mid", "High", "Luxury"]).fillna(0).reset_index())
    by_cat.columns = ["price_category", "count"]
    fig = px.bar(by_cat, x="price_category", y="count", text_auto=True)
    fig.update_layout(xaxis_title="", yaxis_title="Listings")
    st.plotly_chart(fig, use_container_width=True)

# --- Map of listings ---
st.subheader("Listing locations (sample)")
sample = data.sample(min(2000, len(data)), random_state=42)
fig = px.scatter_mapbox(sample, lat="latitude", lon="longitude",
                        color="neighbourhood_group", hover_name="name", zoom=9, height=450)
fig.update_layout(mapbox_style="open-street-map", margin=dict(l=0, r=0, t=0, b=0))
st.plotly_chart(fig, use_container_width=True)

st.divider()
st.subheader("💡 Insights & Recommendations")

# Derive key facts directly from the filtered data
price_by_boro = data.groupby("neighbourhood_group")["price"].median().sort_values(ascending=False)
top_boro, top_price = price_by_boro.index[0], price_by_boro.iloc[0]
low_boro, low_price = price_by_boro.index[-1], price_by_boro.iloc[-1]
top_room = data["room_type"].value_counts().idxmax()
top_room_share = data["room_type"].value_counts(normalize=True).max() * 100
busy_nb = data["neighbourhood"].value_counts().idxmax()

st.markdown(rf"""
- **Most vs least expensive area:** {top_boro} has the highest median price (\${top_price:,.0f}/night), while {low_boro} is the most affordable (\${low_price:,.0f}).
  _Recommendation:_ position premium listings in {top_boro}; target budget-conscious travelers in {low_boro}.
- **Market structure:** {top_room} dominates with {top_room_share:.0f}% of all listings.
  _Recommendation:_ new hosts entering this crowded segment should compete on price, photos, and reviews; consider under-served room types for less competition.
- **Demand hotspot:** {busy_nb} has the most listings — a high-competition, high-demand neighbourhood.
  _Recommendation:_ benchmark pricing here carefully; small price gaps strongly affect bookings.
- **Review gap:** {no_review_pct:.1f}% of listings have no reviews yet.
  _Recommendation:_ help hosts win their first few reviews (intro discounts, fast responses) — listings with reviews convert far better.
- **Availability:** average availability is {data['availability_365'].mean():.0f} days/year.
  _Recommendation:_ low availability can mean high occupancy or part-time hosts — segment accordingly when advising clients.
""")