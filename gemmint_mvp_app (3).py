# GemMint MVP Streamlit App

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Placeholder data
data = [
    {"Card": "Wemby - PSA 10", "Grade": "PSA 10", "Price": 750.00, "Date": "2024-06-01", "Platform": "eBay"},
    {"Card": "Wemby - PSA 10", "Grade": "PSA 10", "Price": 790.00, "Date": "2024-06-15", "Platform": "eBay"},
    {"Card": "Stilltee - Raw", "Grade": "Raw", "Price": 25.00, "Date": "2024-05-29", "Platform": "eBay"},
    {"Card": "Bo Nix PSA 10", "Grade": "PSA 10", "Price": 55.00, "Date": "2024-05-05", "Platform": "eBay"},
    {"Card": "Bo Nix - PSA 10", "Grade": "PSA 10", "Price": 130.00, "Date": "2024-06-10", "Platform": "eBay"},
]

df = pd.DataFrame(data)
df['Date'] = pd.to_datetime(df['Date'])

st.title("GemMint: Sports Card Pricing Tracker")

search_term = st.text_input("Search for a player or card:")
selected_grades = st.multiselect("Select grades to compare:", options=df["Grade"].unique(), default=df["Grade"].unique())

# Filter by search and grade
filtered_df = df.copy()

if search_term:
    filtered_df = filtered_df[filtered_df["Card"].str.contains(search_term, case=False, na=False)]

if selected_grades:
    filtered_df = filtered_df[filtered_df["Grade"].isin(selected_grades)]

# Check before applying date slider
if not filtered_df.empty and 'Date' in filtered_df.columns:
    min_date = filtered_df["Date"].min()
    max_date = filtered_df["Date"].max()
    date_range = st.slider("Select date range", min_value=min_date, max_value=max_date, value=(min_date, max_date))
    filtered_df = filtered_df[(filtered_df["Date"] >= date_range[0]) & (filtered_df["Date"] <= date_range[1])]
else:
    st.warning("No data available to select a date range.")

# Show chart
if not filtered_df.empty:
    fig = px.line(filtered_df, x="Date", y="Price", color="Card", title="Price Trends")
    st.plotly_chart(fig)
else:
    st.info("No data to display.")
