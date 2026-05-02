import streamlit as st
from modules.processor import process_data
import pandas as pd
import plotly.express as px

# ------------------ CONFIG ------------------
st.set_page_config(layout="wide", page_title="Trends & Insights")
st.title("Trends & Insights")

# ------------------ DATA LOADING ------------------
@st.cache_data
def load_data():
    return process_data()

df = load_data()

# ------------------ SIDEBAR ------------------
st.sidebar.header("Filters")
time_range = st.sidebar.selectbox(
    "Select Time Range",
    ["Last 7 Days", "Last 30 Days", "All Time"],
    index=2
)

# ------------------ DATE PROCESSING ------------------
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

# Filter safely
today = pd.Timestamp.today()

if time_range == "Last 7 Days":
    filtered_df = df[df['Date'] >= today - pd.Timedelta(days=7)].copy()
elif time_range == "Last 30 Days":
    filtered_df = df[df['Date'] >= today - pd.Timedelta(days=30)].copy()
else:
    filtered_df = df.copy()

# Warn if bad dates
if filtered_df['Date'].isnull().any():
    st.warning("Some invalid dates were removed.")

# Drop invalid dates
filtered_df = filtered_df.dropna(subset=['Date'])

# ------------------ SUMMARY ------------------
summary = filtered_df.agg({
    "Recovery_Score": ['mean', 'min', 'max'],
    "Sleep_Hours": ['mean', 'min', 'max'],
    "Steps": ['mean', 'min', 'max'],
    "Calories_Burned": ['mean', 'min', 'max'],
}).T

st.subheader("Summary Statistics")
st.dataframe(summary)

# ------------------ MONTHLY TREND ------------------
try:
    # safer: don't mutate original df
    resample_df = filtered_df.set_index('Date')

    monthly_avg_recovery = (
        resample_df
        .resample('M')
        .mean(numeric_only=True)
        .reset_index()
    )

    line_chart_recovery = px.line(
        monthly_avg_recovery,
        x='Date',
        y='Recovery_Score',
        title="Average Monthly Recovery Score",
        labels={'Recovery_Score': 'Average Recovery Score'},
        template="plotly_white"
    )

    st.plotly_chart(line_chart_recovery, use_container_width=True)

except Exception as e:
    st.error(f"Resampling error: {e}")

# ------------------ HISTOGRAMS ------------------
st.subheader("Distributions of Key Metrics")

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(
        px.histogram(filtered_df, x='Steps', title='Steps Distribution'),
        use_container_width=True
    )
    st.plotly_chart(
        px.histogram(filtered_df, x='Recovery_Score', title='Recovery Score Distribution'),
        use_container_width=True
    )

with col2:
    st.plotly_chart(
        px.histogram(filtered_df, x='Calories_Burned', title='Calories Burned Distribution'),
        use_container_width=True
    )
    st.plotly_chart(
        px.histogram(filtered_df, x='Sleep_Hours', title='Sleep Hours Distribution'),
        use_container_width=True
    )