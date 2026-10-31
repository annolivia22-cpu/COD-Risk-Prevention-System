
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="COD Risk Dashboard",
    layout="wide"
)

st.title("COD Risk & RTO Prevention Dashboard")

# Load historical data
df = pd.read_csv("data/orders_sample.csv")

df["final_status"] = (
    df["final_status"].astype(str).str.strip().str.upper()
)

df = df[df["final_status"].isin(["RTO", "DELIVERED"])]

# Calculate values
total_orders = len(df)

rto_orders = (df["final_status"] == "RTO").sum()

delivered = (df["final_status"] == "DELIVERED").sum()

rto_rate = rto_orders / total_orders * 100

# KPI cards
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Orders", total_orders)
col2.metric("Delivered", delivered)
col3.metric("RTO Orders", rto_orders)
col4.metric("RTO Rate", f"{rto_rate:.2f}%")

# Order status chart
st.subheader("Order Status Distribution")

chart_data = pd.DataFrame({
    "Status": ["Delivered", "RTO"],
    "Orders": [delivered, rto_orders]
})

fig = px.pie(
    chart_data,
    names="Status",
    values="Orders",
    hole=0.4
)

st.plotly_chart(fig, use_container_width=True)

# Courier analysis
st.subheader("RTO by Courier")

courier_data = df.groupby("courier")["final_status"].apply(
    lambda x: (x == "RTO").mean() * 100
).reset_index(name="RTO Rate")

fig2 = px.bar(
    courier_data,
    x="courier",
    y="RTO Rate",
    title="RTO Percentage by Courier"
)

st.plotly_chart(fig2, use_container_width=True)


RTO_COST = 169.40
GROSS_MARGIN = 0.62
AVERAGE_ORDER_VALUE = 649
GROSS_PROFIT = AVERAGE_ORDER_VALUE * GROSS_MARGIN
PREPAID_DISCOUNT = 20