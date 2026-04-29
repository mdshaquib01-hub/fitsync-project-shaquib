import streamlit as st
from modules.processor import process_data
import pandas as pd
import plotly.express as px

# Set up the page configuration
st.set_page_config(layout="wide", page_title="FitSync")

# Add a title to the app
st.title("FitSync - Personal Health Analytics")

# Process and load the data
df = process_data()

# Sidebar for filters
st.sidebar.header("Filters")
time_range = st.sidebar.selectbox(
    "Select Time Range",
    options=["Last 7 Days", "Last 30 Days", "All Time"],
    index=2
)

# Filter the dataframe based on the selected time range
if time_range == "Last 7 Days":
    filtered_df = df[df['Date'] >= pd.to_datetime('today') - pd.Timedelta(days=7)]
elif time_range == "Last 30 Days":
    filtered_df = df[df['Date'] >= pd.to_datetime('today') - pd.Timedelta(days=30)]
else:
    filtered_df = df

# Re-calculate average values from the filtered DataFrame
average_steps = filtered_df['Steps'].mean()
average_sleep_hours = filtered_df['Sleep_Hours'].mean()
average_recovery_score = filtered_df['Recovery_Score'].mean()

# Display metrics in the columns
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Average Steps", value=int(average_steps), delta=None)

with col2:
    st.metric(label="Average Sleep Hours", value=f"{average_sleep_hours:.1f}", delta=None)

with col3:
    st.metric(label="Average Recovery Score", value=f"{average_recovery_score:.1f}", delta=None)

# Create charts
# Chart for Recovery Score & Sleep Trend
dual_line_chart = px.line(
    filtered_df, x='Date', y=['Recovery_Score', 'Sleep_Hours'],
    title="Recovery Score & Sleep Trend",
    labels={'value': 'Score/Hours', 'variable': 'Metric'},
    template="plotly_white"
)

# Chart for Recovery Score vs Daily Steps
scatter_plot_steps = px.scatter(
    filtered_df, x='Steps', y='Recovery_Score', color='Sleep_Hours',
    title="Recovery Score vs Daily Steps",
    labels={'color': 'Sleep Hours'},
    template="plotly_white"
)

# Chart for Recovery Score vs Resting Heart Rate
scatter_plot_heart_rate = px.scatter(
    filtered_df, x='Heart_Rate_bpm', y='Recovery_Score',
    title="Recovery Score vs Resting Heart Rate",
    labels={'x': 'Resting Heart Rate (BPM)'},
    template="plotly_white"
)

# Chart for Daily Calories Burned Trend
line_chart_calories = px.line(
    filtered_df, x='Date', y='Calories_Burned',
    title="Daily Calories Burned Trend",
    labels={'Calories_Burned': 'Calories Burned'},
    template="plotly_white"
)

# Display the dual column charts
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(dual_line_chart, use_container_width=True)

with col2:
    st.plotly_chart(scatter_plot_steps, use_container_width=True)

# Display the second set of dual column charts
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(scatter_plot_heart_rate, use_container_width=True)

with col2:
    st.plotly_chart(line_chart_calories, use_container_width=True)
