
# GemMint MVP Streamlit App
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Placeholder data
data = [
    {"Card": "Wemby - PSA 10", "Grade": "PSA 10", "Price": 750.00, "Date": "2024-06-01", "Platform": "eBay"},
    {"Card": "Wemby - PSA 10", "Grade": "PSA 10", "Price": 790.00, "Date": "2024-06-15", "Platform": "eBay"},
    {"Card": "Stützle - Raw", "Grade": "Raw", "Price": 25.00, "Date": "2024-05-20", "Platform": "eBay"},
    {"Card": "Bo Nix - PSA 9", "Grade": "PSA 9", "Price": 55.00, "Date": "2024-05-05", "Platform": "eBay"},
    {"Card": "Bo Nix - PSA 10", "Grade": "PSA 10", "Price": 130.00, "Date": "2024-06-10", "Platform": "eBay"},
]
df = pd.DataFrame(data)
df['Date'] = pd.to_datetime(df['Date'])

st.title("GemMint: Sports Card Pricing Tracker")

# Search
search_term = st.text_input("Search for a player or card:", "Wemby")
filtered_df = df[df['Card'].str.contains(search_term, case=False)]

# Grade filter
grades = filtered_df['Grade'].unique().tolist()
selected_grades = st.multiselect("Select grades to compare:", grades, default=grades)
plot_df = filtered_df[filtered_df['Grade'].isin(selected_grades)]

# Date range filter
min_date = plot_df['Date'].min()
max_date = plot_df['Date'].max()
date_range = st.slider("Select date range:", min_value=min_date, max_value=max_date,
                       value=(min_date, max_date))
plot_df = plot_df[(plot_df['Date'] >= date_range[0]) & (plot_df['Date'] <= date_range[1])]

# Graph
if not plot_df.empty:
    fig = px.line(plot_df, x='Date', y='Price', color='Grade', markers=True,
                  title=f"Price Trends for '{search_term.title()}'")
    st.plotly_chart(fig)
else:
    st.info("No data to display. Try a different search or grade.")

# CSV Export
st.download_button("Download CSV", plot_df.to_csv(index=False), file_name="card_prices.csv")

# GPT Insights placeholder
st.markdown("---")
st.subheader("💡 GPT Buy/Sell/Hold Insight")
st.write("Based on market trends and recent sales, consider holding your high-grade copies until closer to the next season. PSA 10 variants have shown consistent upward momentum.")

# Alerts - placeholder structure
st.markdown("---")
st.subheader("🔔 Set a Price Alert")
st.text_input("Enter your email:")
st.number_input("Alert me when this card goes below (CAD):", min_value=0.0, step=1.0)
st.button("Set Alert")
