
import streamlit as st 
import pandas as pd 
import numpy as np 
import plotly.express as px 
import plotly.graph_objects as go

# Load the cleaned data
# df_us = pd.read_csv('sample_cleaned_data.csv')
url = "https://drive.google.com/uc?id=13BDfNE6c4fZKIfzTbvRZXvxpkQar9nqn"
df_us = pd.read_csv(url, low_memory=False)  

# convert datetime columns
df_us['Start_Time'] = pd.to_datetime(df_us['Start_Time'])
df_us['Hour'] = df_us['Start_Time'].dt.hour
df_us['DayOfWeek'] = df_us['Start_Time'].dt.day_name()
df_us['Month'] = df_us['Start_Time'].dt.month

# Streamlit page configuration
st.set_page_config(page_title="US Accidents Dashboard", layout="wide")
st.title("US Accidents Dashboard")

# Sidebar filters by state and severity
st.sidebar.header("Filters")
all_states = sorted(df_us['State'].unique())
top_states = df_us['State'].value_counts().head(5).index.tolist() 
selected_states = st.sidebar.multiselect("Select States:", all_states, top_states)
selected_severity = st.sidebar.multiselect("Select Severity:", sorted(df_us['Severity'].unique()), default=sorted(df_us['Severity'].unique()))

# Filter data based on selections
filtered_df_us = df_us[(df_us['State'].isin(selected_states)) & (df_us['Severity'].isin(selected_severity))]

# KPI Metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Accidents", f"{len(filtered_df_us)}")
with col2:
    st.metric("States Covered", filtered_df_us['State'].nunique())
with col3:
    st.metric("Cities Covered", filtered_df_us['City'].nunique())
with col4:
    st.metric("Avg Duration (min)", f"{filtered_df_us['Duration_Minutes'].mean():.1f}")


# State and Severity
col1, col2 = st.columns(2)

with col1:
    state_data = filtered_df_us['State'].value_counts().head(10)
    fig_states = px.bar(x=state_data.values, y=state_data.index, 
                        title="Top 10 States", labels={'x': 'Accidents', 'y': 'State'},
                        orientation='h')
    st.plotly_chart(fig_states, use_container_width=True)

with col2:
    severity_labels = {1: 'Low', 2: 'Med', 3: 'High', 4: 'Critical'}
    sev_data = filtered_df_us['Severity'].value_counts().sort_index()
    sev_names = [severity_labels[i] for i in sev_data.index]
    fig_severity = px.pie(values=sev_data.values, names=sev_names,
                          title="Severity Distribution",
                          color_discrete_sequence=['#2ECC71', '#F39C12', '#E74C3C', '#8B0000'])
    st.plotly_chart(fig_severity, use_container_width=True)


# Hour and Day
col1, col2 = st.columns(2)

with col1:
    hours = filtered_df_us['Hour'].value_counts().sort_index()
    fig_hours = go.Figure(data=[go.Scatter(x=hours.index, y=hours.values, mode='lines+markers', fill='tozeroy')])
    fig_hours.update_layout(title="Accidents by Hour", xaxis_title="Hour", yaxis_title="Count")
    st.plotly_chart(fig_hours, use_container_width=True)

with col2:
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day = filtered_df_us['DayOfWeek'].value_counts().reindex(day_order)
    fig_day = px.bar(x=day_order, y=day.values, title="Accidents by Day", labels={'x': 'Day', 'y': 'Accidents'})
    st.plotly_chart(fig_day, use_container_width=True)

# Top Cities and Weather
col1, col2 = st.columns(2)

with col1:
    city_data = filtered_df_us['City'].value_counts().head(5)
    fig_cities = px.bar(x=city_data.values, y=city_data.index, title="Top 5 Cities into states you selected ", labels={'x': 'Accidents', 'y': 'City'})
    st.plotly_chart(fig_cities, use_container_width=True)

with col2:
    weather_data = filtered_df_us['Weather_Condition'].value_counts().head(5)
    fig_weather = px.bar(x=weather_data.values, y=weather_data.index, title="Top 5 Weather Conditions", labels={'x': 'Accidents', 'y': 'Weather'})
    st.plotly_chart(fig_weather, use_container_width=True)


# Temperature and Visibility
col1, col2 = st.columns(2)

with col1:
    filtered_df_us['Temp_Range'] = pd.cut(filtered_df_us['Temperature(F)'],
                                       bins=[-30, 0, 30, 50, 70, 90, 200],
                                       labels=['Freezing', 'Cold', 'Cool', 'Warm', 'Hot', 'Very Hot'])
    temp_data = filtered_df_us['Temp_Range'].value_counts().sort_index()
    fig_temp = px.bar(x=temp_data.index, y=temp_data.values, title="Accidents by Temperature",
                      labels={'x': 'Temperature Range', 'y': 'Accidents'})
    st.plotly_chart(fig_temp, use_container_width=True)

with col2:
    filtered_df_us['Visibility_Range'] = pd.cut(filtered_df_us['Visibility(mi)'],
                                             bins=[0, 0.5, 1, 5, 10, 50],
                                             labels=['Very Low', 'Low', 'Med', 'Good', 'Excellent'])
    vis_data = filtered_df_us['Visibility_Range'].value_counts().sort_index()
    fig_vis = px.bar(x=vis_data.index, y=vis_data.values, title="Accidents by Visibility",
                     labels={'x': 'Visibility Level', 'y': 'Accidents'})
    st.plotly_chart(fig_vis, use_container_width=True)


# duration
col1, col2 = st.columns(2)

with col1:
    monthly = filtered_df_us['Month'].value_counts().sort_index()
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    month_labels = [month_names[i-1] for i in monthly.index]
    fig_monthly = go.Figure(data=[go.Scatter(x=month_labels, y=monthly.values, mode='lines+markers', fill='tozeroy')])
    fig_monthly.update_layout(title="Monthly", xaxis_title="Month", yaxis_title="Accidents")
    st.plotly_chart(fig_monthly, use_container_width=True)



# Data Table
st.subheader("Data")
st.dataframe(filtered_df_us[['Start_Time', 'State', 'City', 'Severity', 'Temperature(F)', 
                          'Visibility(mi)', 'Weather_Condition', 'Duration_Minutes']].head())

st.write('---')
# total records 
st.header("\nTotal Records Report")
st.write(f"- Total records in Dataset: {len(df_us)}")
st.write(f"- Total records displayed: {len(filtered_df_us)}")
st.write(f"- Date range: {df_us['Start_Time'].min().strftime('%Y-%m-%d')} to {df_us['Start_Time'].max().strftime('%Y-%m-%d')}")
st.write(f"- Unique states: {df_us['State'].nunique()}")
st.write(f"- Unique severity Levels: {df_us['Severity'].nunique()}")
st.write(f"- Unique cities: {df_us['City'].nunique()}")
st.write(f"- Unique Weather conditions: {df_us['Weather_Condition'].nunique()}")
st.write(f"- Average Duration for accidents: {filtered_df_us['Duration_Minutes'].mean():.2f} minutes")
st.write(f"- Average Visibility drivers: {filtered_df_us['Visibility(mi)'].mean():.2f} miles")
st.write(f"- Average Temperature: {filtered_df_us['Temperature(F)'].mean():.1f}°F")


# Severity statistics
st.subheader("\nSeverity Breakdown:")
severity_labels = {1: 'Low', 2: 'Med', 3: 'High', 4: 'Critical'}
severity_report = filtered_df_us['Severity'].value_counts().sort_index()
for sev_level, count in severity_report.items():
    percentage = (count / len(filtered_df_us)) * 100
    st.write(f"- {severity_labels[sev_level]}: {count} ({percentage:.2f}%)")

# Top 5 Covered States statistics as per selection
st.subheader("\nCovered States Statistics:")
state_report = filtered_df_us['State'].value_counts().nlargest()
for (state, count) in state_report.items():
    percentage = (count / len(filtered_df_us)) * 100
    st.write(f"- {state}: {count} ({percentage:.2f}%)")

# Top 5 Covered States statistics as per selection
st.subheader("\nCovered Cities Statistics:")
city_report = filtered_df_us['City'].value_counts().nlargest()
for (city, count) in city_report.items():
    percentage = (count / len(filtered_df_us)) * 100
    st.write(f"- {city}: {count} ({percentage:.2f}%)")

# Weather conditions statistics
st.subheader("Top Weather Conditions")
weather_report = filtered_df_us['Weather_Condition'].value_counts().head(5)
for weather, count in weather_report.items():
    percentage = (count / len(filtered_df_us)) * 100
    st.write(f"- {weather}: {count:,} ({percentage:.2f}%)")





