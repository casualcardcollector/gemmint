
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Placeholder data
data = [
    {"Card": "Wemby - PSA 10", "Grade": "PSA 10", "Price": 750.00, "Date": "2024-06-01", "Platform": "eBay"},
    {"Card": "Wemby - PSA 10", "Grade": "PSA 10", "Price": 790.00, "Date": "2024-06-15", "Platform": "eBay"},
    {"Card": "Wemby - PSA 10", "Grade": "PSA 10", "Price": 798.00, "Date": "2024-06-19", "Platform": "eBay"},
    {"Card": "Stiltlee Raw", "Grade": "Raw", "Price": 25.00, "Date": "2024-06-20", "Platform": "eBay"},
    {"Card": "Bo Nix - PSA 9", "Grade": "PSA 9", "Price": 55.00, "Date": "2024-06-05", "Platform": "eBay"},
    {"Card": "Bo Nix - PSA 10", "Grade": "PSA 10", "Price": 130.00, "Date": "2024-06-10", "Platform": "eBay"},
]

df = pd.DataFrame(data)
df['Date'] = pd.to_datetime(df['Date'])

st.title("GemMint: Sports Card Pricing Tracker")

# Sidebar filters
selected_card = st.text_input("Search for a player or card:", "")
available_grades = df['Grade'].unique().tolist()
selected_grades = st.multiselect("Select grades to compare:", available_grades, default=available_grades)

# Filter data
filtered_df = df.copy()
if selected_card:
    filtered_df = filtered_df[filtered_df['Card'].str.contains(selected_card, case=False)]

if selected_grades:
    filtered_df = filtered_df[filtered_df['Grade'].isin(selected_grades)]

if not filtered_df.empty:
    min_date = filtered_df['Date'].min()
    max_date = filtered_df['Date'].max()

    if min_date <= max_date:
        date_range = st.slider("Select date range:", min_value=min_date, max_value=max_date, value=(min_date, max_date))
        filtered_df = filtered_df[(filtered_df['Date'] >= date_range[0]) & (filtered_df['Date'] <= date_range[1])]

        fig = px.line(filtered_df, x='Date', y='Price', color='Card', markers=True, title="Card Prices Over Time")
        st.plotly_chart(fig)

        st.dataframe(filtered_df)
    else:
        st.warning("Invalid date range in the filtered data.")
else:
    st.warning("No data available for the selected filters.")
