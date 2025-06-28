
# GemMint MVP Streamlit App
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Placeholder data
data = [
    {"Card": "Wemby - PSA 10", "Grade": "PSA 10", "Price": 750.00, "Date": "2024-06-01", "Platform": "eBay"},
    {"Card": "Wemby - PSA 10", "Grade": "PSA 10", "Price": 790.00, "Date": "2024-06-15", "Platform": "eBay"},
    {"Card": "Stilltee - Raw", "Grade": "Raw", "Price": 25.00, "Date": "2024-06-20", "Platform": "eBay"},
    {"Card": "Bo Nix - PSA 10", "Grade": "PSA 10", "Price": 55.00, "Date": "2024-05-05", "Platform": "eBay"},
    {"Card": "Bo Nix - PSA 10", "Grade": "PSA 10", "Price": 130.00, "Date": "2024-06-10", "Platform": "eBay"},
]

df = pd.DataFrame(data)
df['Date'] = pd.to_datetime(df['Date'])

# Streamlit layout
st.title("GemMint: Sports Card Pricing Tracker")

# Filters
card_filter = st.text_input("Search for a player or card:", "")
grade_filter = st.multiselect("Select grades to compare:", options=df['Grade'].unique(), default=df['Grade'].unique())

# Ensure there's at least one row after filtering to set slider bounds
filtered_df = df[df['Grade'].isin(grade_filter)]
if not filtered_df.empty:
    min_date = filtered_df['Date'].min()
    max_date = filtered_df['Date'].max()
    date_range = st.slider("Select date range", min_value=min_date, max_value=max_date, value=(min_date, max_date))
else:
    st.warning("No data available for the selected filters.")
    st.stop()

# Apply filters
filtered_df = filtered_df[
    filtered_df['Card'].str.contains(card_filter, case=False) &
    (filtered_df['Date'] >= date_range[0]) &
    (filtered_df['Date'] <= date_range[1])
]

# Output
if not filtered_df.empty:
    fig = px.line(filtered_df, x='Date', y='Price', color='Card', markers=True, title="Price Over Time")
    st.plotly_chart(fig)
    st.dataframe(filtered_df)
else:
    st.write("No matching data found.")
