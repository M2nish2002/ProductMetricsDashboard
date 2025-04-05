import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta

st.set_page_config(page_title="Product Metrics Dashboard", layout="wide")
st.title("📊 Product Metrics Dashboard")

# Simulate dataset
np.random.seed(42)
n_users = 1000
start_date = datetime(2024, 1, 1)
data = {
    "user_id": range(1, n_users + 1),
    "signup_date": [start_date + timedelta(days=np.random.randint(0, 90)) for _ in range(n_users)],
    "last_active_date": [start_date + timedelta(days=np.random.randint(20, 120)) for _ in range(n_users)],
    "pages_viewed": np.random.poisson(10, n_users),
    "conversions": np.random.binomial(1, 0.3, n_users)
}
df = pd.DataFrame(data)

# Filter for active users in the last 30 days
today = datetime(2025, 4, 1)
df["is_active"] = df["last_active_date"] >= (today - timedelta(days=30))

# DAU Calculation
date_range = pd.date_range(start=start_date, end=today)
dau = pd.DataFrame({"date": date_range})
dau["active_users"] = dau["date"].apply(lambda d: df[df["last_active_date"] == d].shape[0])

# Retention: Percent of users still active 30+ days after signup
retention_df = df.copy()
retention_df["retained"] = (retention_df["last_active_date"] - retention_df["signup_date"]).dt.days >= 30
retention_rate = retention_df["retained"].mean()

# Conversion rate
conversion_rate = df["conversions"].mean()

# Sidebar filters
date_selection = st.sidebar.date_input("Filter by Signup Date", [])
if date_selection:
    df = df[(df["signup_date"] >= pd.to_datetime(date_selection[0])) & (df["signup_date"] <= pd.to_datetime(date_selection[1]))]

# Dashboard components
col1, col2, col3 = st.columns(3)
col1.metric("Conversion Rate", f"{conversion_rate:.2%}")
col2.metric("30-Day Retention Rate", f"{retention_rate:.2%}")
col3.metric("Active Users (30d)", df["is_active"].sum())

st.subheader("📈 Daily Active Users")
fig_dau = px.line(dau, x="date", y="active_users", title="Daily Active Users Over Time")
st.plotly_chart(fig_dau, use_container_width=True)

st.subheader("🔄 Conversion Distribution")
fig_conv = px.histogram(df, x="conversions", title="Conversions", labels={"conversions": "Converted"})
st.plotly_chart(fig_conv, use_container_width=True)

st.subheader("📉 Pages Viewed Distribution")
fig_pages = px.box(df, y="pages_viewed", title="Pages Viewed Per User")
st.plotly_chart(fig_pages, use_container_width=True)
