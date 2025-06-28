
import streamlit as st
import pandas as pd
from datetime import datetime

# Sample data loading
@st.cache_data
def load_data():
    df = pd.read_csv("card_data.csv", parse_dates=["date"])
    df["grade"] = df["grade"].astype(str)
    return df

df = load_data()

# Page title
st.title("GemMint: Sports Card Pricing Tracker")

# Search box
search_term = st.text_input("Search for a player or card:")

# Grade selection
grades = df["grade"].unique().tolist()
selected_grades = st.multiselect("Select grades to compare:", grades, default=grades)

# Filter based on search and grade
filtered_df = df[
    df["card"].str.contains(search_term, case=False, na=False)
    & df["grade"].isin(selected_grades)
]

# Check if filtered_df is not empty before computing date range
if not filtered_df.empty:
    min_date = filtered_df["date"].min()
    max_date = filtered_df["date"].max()
    date_range = st.slider(
        "Select date range:", min_value=min_date, max_value=max_date,
        value=(min_date, max_date)
    )

    # Filter by date range
    filtered_df = filtered_df[
        (filtered_df["date"] >= date_range[0]) & (filtered_df["date"] <= date_range[1])
    ]

    # Display chart
    st.line_chart(filtered_df.pivot_table(index="date", columns="grade", values="price"))
else:
    st.warning("No data matches your criteria.")
