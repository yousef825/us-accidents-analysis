
import streamlit as st 
import pandas as pd 
import numpy as np 
import plotly.express as px 
import plotly.graph_objects as go

# Load the cleaned data
df_us = pd.read_csv('D:/mid_project/data/us_accidents_cleaned.csv')

# convert datetime columns
df_us['Start_Time'] = pd.to_datetime(df_us['Start_Time'])
df_us['Hour'] = df_us['Start_Time'].dt.hour
df_us['DayOfWeek'] = df_us['Start_Time'].dt.day_name()
df_us['Month'] = df_us['Start_Time'].dt.month
df_us['IsWeekday'] = df_us['Start_Time'].dt.weekday < 5

# Streamlit page configuration
st.set_page_config(page_title="US Accidents Dashboard", layout="wide")
st.title("US Accidents Dashboard")

# Sidebar filters
st.sidebar.header("Filters")
all_states = sorted(df_us['State'].unique())
top_states = ["All States"] + df_us['State'].value_counts().head(5).index.tolist()
selected_states = st.sidebar.multiselect("Select States:", ["All States"] + all_states, default=["All States"])

# Handle "All States" selection
if "All States" in selected_states:
    selected_states = all_states
    
selected_severity = st.sidebar.multiselect("Select Severity:", sorted(df_us['Severity'].unique()), default=sorted(df_us['Severity'].unique()))

# Filter data based on selections
filtered_df = df_us[(df_us['State'].isin(selected_states)) & (df_us['Severity'].isin(selected_severity))]

# Sidebar KPIs
st.sidebar.markdown("---")
st.sidebar.header("Key Metrics")
col1, col2 = st.sidebar.columns(2)
with col1:
    st.metric("Total Accidents", f"{len(filtered_df):,}")
    st.metric("Avg Duration (min)", f"{filtered_df['Duration_Minutes'].mean():.1f}")
    st.metric("Avg Visibility (mi)", f"{filtered_df['Visibility(mi)'].mean():.2f}")
with col2:
    st.metric("Avg Temp (°F)", f"{filtered_df['Temperature(F)'].mean():.1f}")
    st.metric("Cities Covered", f"{filtered_df['City'].nunique()}")
    sev2_pct = (len(filtered_df[filtered_df['Severity'] == 2]) / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
    st.metric("Severity", f"{sev2_pct:.1f}%")
#--------------------------------------------------------------------------------------------------------------------------
# Sidebar Key Insights

# st.sidebar.markdown("---")
# st.sidebar.header("Key Insights")
# top3_states_pct = (df_us[df_us['State'].isin(['CA', 'TX', 'FL'])].shape[0] / len(df_us) * 100)
# st.sidebar.info(f"**CA + TX + FL = {top3_states_pct:.1f}%** of all accidents")

# hourly_peak = filtered_df['Hour'].value_counts()
# st.sidebar.info("**Peak hours: 6–8 AM & 3–6 PM**")

# fair_weather = len(filtered_df[filtered_df['Weather_Condition'].str.contains('Fair|Clear', case=False, na=False)]) / len(filtered_df) * 100 if len(filtered_df) > 0 else 0
# st.sidebar.info(f"**Fair weather dominates** (~{fair_weather:.0f}% of accidents)")

# warm_temp = len(filtered_df[(filtered_df['Temperature(F)'] >= 50) & (filtered_df['Temperature(F)'] <= 80)]) / len(filtered_df) * 100 if len(filtered_df) > 0 else 0
# st.sidebar.info(f"**Warm temps (50–80°F)** see most incidents (~{warm_temp:.0f}%)")

# avg_duration = filtered_df['Duration_Minutes'].mean()
# st.sidebar.info(f"**Avg incident duration:** {avg_duration:.0f} minutes")

# high_severity_pct = (len(filtered_df[filtered_df['Severity'] >= 3]) / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
# st.sidebar.info(f"**High severity (3–4): {high_severity_pct:.1f}%** of incidents")

# low_visibility = len(filtered_df[filtered_df['Visibility(mi)'] < 5]) / len(filtered_df) * 100 if len(filtered_df) > 0 else 0
# st.sidebar.info(f"**Poor visibility (<5 mi)** in {low_visibility:.0f}% of cases")

#--------------------------------------------------------------------------------------------------------------------------


tab1, tab2, tab3, tab4, tab5 = st.tabs(["Overview", "Temporal", "Weather & Conditions","Report","Risk Analysis"])

# TAB 1: OVERVIEW
state_names = {
    'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas', 'CA': 'California',
    'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware', 'FL': 'Florida', 'GA': 'Georgia',
    'HI': 'Hawaii', 'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa',
    'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland',
    'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi', 'MO': 'Missouri',
    'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada', 'NH': 'New Hampshire', 'NJ': 'New Jersey',
    'NM': 'New Mexico', 'NY': 'New York', 'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio',
    'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina',
    'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VT': 'Vermont',
    'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia', 'WI': 'Wisconsin', 'WY': 'Wyoming'
}

with tab1:
    st.header("Overview")
    col1, col2 = st.columns(2)
    
    with col1:
        state_data = filtered_df['State'].value_counts().head(10)
        state_labels = [state_names.get(state, state) for state in state_data.index]
        fig_states = px.bar(x=state_data.values, y=state_labels, 
                            title="Top 10 States by Accidents", labels={'x': 'Accidents', 'y': 'State'},
                            orientation='h', color=state_data.values, color_continuous_scale='Viridis')
        st.plotly_chart(fig_states, use_container_width=True)
        
        top3_states_pct = (filtered_df[filtered_df['State'].isin(['CA', 'TX', 'FL'])].shape[0] / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
        st.info(f"**CA + TX + FL = {top3_states_pct:.1f}%** of filtered accidents")
    
    
    
    with col2:
        severity_labels = {1: 'Low', 2: 'Med', 3: 'High', 4: 'Critical'}
        sev_data = filtered_df['Severity'].value_counts().sort_index()
        sev_names = [severity_labels[i] for i in sev_data.index]
        fig_severity = px.pie(values=sev_data.values, names=sev_names,
                              title="Severity Distribution",
                              color_discrete_sequence=['#2ECC71', '#F39C12', '#E74C3C', '#8B0000'])
        st.plotly_chart(fig_severity, use_container_width=True)
        
        high_severity_pct = (len(filtered_df[filtered_df['Severity'] >= 3]) / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
        st.info(f"**High severity (3–4): {high_severity_pct:.1f}%** of incidents")
        



    col1, col2 = st.columns(2)
    
    with col1:
        city_data = filtered_df['City'].value_counts().head(10)
        fig_cities = px.bar(x=city_data.values, y=city_data.index,
                            title="Top 10 Cities by Accidents", labels={'x': 'Accidents', 'y': 'City'},
                            orientation='h', color=city_data.values, color_continuous_scale='Blues')
        st.plotly_chart(fig_cities, use_container_width=True)
        
        top_3_cities = city_data.head(3)
        top_3_pct = (top_3_cities.sum() / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
        top_3_names = ', '.join(top_3_cities.index.tolist())
        st.info(f"**Top 3 cities ({top_3_names}) = {top_3_pct:.1f}%** of filtered accidents")
    
    with col2:
        day_night = filtered_df['Hour'].apply(lambda x: 'Day (6 AM - 6 PM)' if 6 <= x < 18 else 'Night (6 PM - 6 AM)')
        dn_counts = day_night.value_counts()
        fig_daynight = px.pie(values=dn_counts.values, names=dn_counts.index,
                              title="Day vs Night Accidents",
                              color_discrete_sequence=['#FFD700', '#191970'])
        st.plotly_chart(fig_daynight, use_container_width=True)

# TAB 2: TEMPORAL
with tab2:
    st.header("Temporal Patterns")
    col1, col2 = st.columns(2)
    
    with col1:
        hourly = filtered_df['Hour'].value_counts().sort_index()
        fig_hourly = go.Figure(data=[go.Scatter(x=hourly.index, y=hourly.values, mode='lines+markers', fill='tozeroy', line=dict(color='#1f77b4'))])
        fig_hourly.update_layout(title="Accidents by Hour of Day", xaxis_title="Hour", yaxis_title="Count", hovermode='x unified')
        st.plotly_chart(fig_hourly, use_container_width=True)
        
        hourly_peak = filtered_df['Hour'].value_counts()
        st.info("**Peak hours: 6–8 AM & 3–5 PM**")
        
    
    with col2:
        daily = filtered_df['DayOfWeek'].value_counts()
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        daily = daily.reindex(day_order)
        
        fig_daily = px.bar(x=day_order, y=daily.values, 
                   title="Accidents by Day of Week",
                   labels={'x': 'Day', 'y': 'Accidents'},
                   color=day_order,
                   color_discrete_map={day: '#4ECDC4' if day in ['Saturday', 'Sunday'] else '#FF6B6B' for day in day_order})
        st.plotly_chart(fig_daily, use_container_width=True)
        
        weekday_accidents = len(filtered_df[filtered_df['IsWeekday']]) / len(filtered_df) * 100 if len(filtered_df) > 0 else 0
        st.info(f"**Weekdays: {weekday_accidents:.0f}%** vs **Weekends: {100-weekday_accidents:.0f}%**")
    
    avg_duration = filtered_df['Duration_Minutes'].mean()
    st.info(f"**Avg incident duration:** {avg_duration:.0f} minutes")
        

    
    monthly = filtered_df['Month'].value_counts().sort_index()
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    month_labels = [month_names[i-1] for i in monthly.index]
    fig_monthly = go.Figure(data=[go.Scatter(x=month_labels, y=monthly.values, mode='lines+markers', fill='tozeroy', line=dict(color='#2ecc71'))])
    fig_monthly.update_layout(title="Monthly Trends", xaxis_title="Month", yaxis_title="Accidents", hovermode='x unified')
    st.plotly_chart(fig_monthly, use_container_width=True)
    
    

# TAB 3: WEATHER & CONDITIONS
with tab3:
    st.header("Weather & Road Conditions")
            
    filtered_df['Temp_Range'] = pd.cut(filtered_df['Temperature(F)'],
                                       bins=[-30, 0, 32, 50, 70, 85, 105],
                                       labels=['Freezing', 'Cold', 'Cool', 'Warm', 'Hot', 'Very Hot'])
    temp_data = filtered_df['Temp_Range'].value_counts().sort_index()
    fig_temp = px.bar(x=temp_data.index, y=temp_data.values, title="Accidents by Temperature Range",
                      labels={'x': 'Temperature Range', 'y': 'Accidents'}, color=temp_data.index,
                      color_discrete_sequence=['#4169E1', '#87CEEB', '#90EE90', '#FFD700', '#FF8C00', '#FF4500'])
    st.plotly_chart(fig_temp, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        weather_data = filtered_df['Weather_Condition'].value_counts().head(10)
        fig_weather = px.bar(x=weather_data.values, y=weather_data.index,
                             title="Top 10 Weather Conditions", labels={'x': 'Accidents', 'y': 'Weather'},
                             orientation='h', color=weather_data.values, color_continuous_scale='Sunset')
        st.plotly_chart(fig_weather, use_container_width=True)
    
        fair_weather = len(filtered_df[filtered_df['Weather_Condition'].str.contains('Fair|Clear', case=False, na=False)]) / len(filtered_df) * 100 if len(filtered_df) > 0 else 0
        st.info(f"**Fair weather dominates** (~{fair_weather:.0f}% of accidents)")
    
     
    
    with col2:
    
        filtered_df['Visibility_Range'] = pd.cut(filtered_df['Visibility(mi)'],
                                                 bins=[0, 0.5, 1, 5, 10, 50],
                                                 labels=['Very Low', 'Low', 'Med', 'Good', 'Excellent'])
        vis_data = filtered_df['Visibility_Range'].value_counts().sort_index()
        fig_vis = px.bar(x=vis_data.index, y=vis_data.values, title="Accidents by Visibility Level",
                         labels={'x': 'Visibility', 'y': 'Accidents'}, color=vis_data.index,
                         color_discrete_sequence=['#8B0000', '#FF4500', '#FFD700', '#90EE90', '#006400'])
        st.plotly_chart(fig_vis, use_container_width=True)
   
        low_visibility = len(filtered_df[filtered_df['Visibility(mi)'] < 5]) / len(filtered_df) * 100 if len(filtered_df) > 0 else 0
        st.info(f"**Poor visibility (<5 mi)** in {low_visibility:.0f}% of cases")
     
        

        
# TAB 4: REPORT
with tab4:
    st.header("Report")
    
    st.subheader("Dataset Summary")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(f"**Total Records:** {len(df_us):,}")
        # st.write(f"**Displayed:** {len(filtered_df):,}")
    with col2:
        st.write(f"**Unique States:** {df_us['State'].nunique()}")
        st.write(f"**Unique Cities:** {df_us['City'].nunique()}")
    with col3:
        date_min = df_us['Start_Time'].min().strftime('%Y-%m-%d')
        date_max = df_us['Start_Time'].max().strftime('%Y-%m-%d')
        st.write(f"**Date Range:** {date_min} to {date_max}")
        st.write(f"**Weather Types:** {df_us['Weather_Condition'].nunique()}")
    
    st.markdown("---")
    st.subheader("Severity Breakdown")
    severity_labels = {1: 'Low', 2: 'Med', 3: 'High', 4: 'Critical'}
    severity_report = filtered_df['Severity'].value_counts().sort_index()
    cols = st.columns(len(severity_report))
    for idx, (sev_level, count) in enumerate(severity_report.items()):
        cols[idx].metric(severity_labels[sev_level], f"{count:,}")
    
    st.markdown("---")
    st.subheader("Top 10 States Statistics")
    state_report = filtered_df['State'].value_counts().head(10)
    state_df = pd.DataFrame({
        'State': [state_names.get(state, state) for state in state_report.index],
        'Count': state_report.values,
        'Percentage': (state_report.values / len(filtered_df) * 100).round(2)
    })
    st.dataframe(state_df, use_container_width=True)
    
    st.markdown("---")
    st.subheader("Top 10 Cities Statistics")
    city_report = filtered_df['City'].value_counts().head(10)
    city_df = pd.DataFrame({
        'City': city_report.index,
        'Count': city_report.values,
        'Percentage': (city_report.values / len(filtered_df) * 100).round(2)
    })
    st.dataframe(city_df, use_container_width=True)
    
    st.markdown("---")
    st.subheader("Top 10 Weather Conditions")
    weather_report = filtered_df['Weather_Condition'].value_counts().head(10)
    weather_df = pd.DataFrame({
        'Weather': weather_report.index,
        'Count': weather_report.values,
        'Percentage': (weather_report.values / len(filtered_df) * 100).round(2)
    })
    st.dataframe(weather_df, use_container_width=True)
    
    st.markdown("---")
    st.subheader("Sample Data (First 50 Records)")
    st.dataframe(filtered_df[['Start_Time', 'State', 'City', 'Severity', 'Temperature(F)', 
                              'Visibility(mi)', 'Weather_Condition', 'Duration_Minutes']].head(50), use_container_width=True)
    
    
# TAB 5: RISK ANALYSIS
with tab5:
    st.header("Risk Analysis")
    
    st.markdown("""
    ### Why Accidents Occur in Warm Temperature & Good Visibility?
    
    This analysis focuses on conditions where temperature is warm (50–80°F) and visibility is good (5–10 mi), 
    which paradoxically see high accident rates despite seemingly safe conditions.
    """)
    
    # Filter data for warm temp and good visibility
    warm_temp_df = filtered_df[(filtered_df['Temperature(F)'] >= 50) & (filtered_df['Temperature(F)'] <= 80)]
    good_vis_df = filtered_df[(filtered_df['Visibility(mi)'] >= 5) & (filtered_df['Visibility(mi)'] <= 10)]
    warm_good_df = filtered_df[
        (filtered_df['Temperature(F)'] >= 50) & (filtered_df['Temperature(F)'] <= 80) &
        (filtered_df['Visibility(mi)'] >= 5) & (filtered_df['Visibility(mi)'] <= 10)
    ]
    
    st.subheader("Key Statistics")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Warm Temp Accidents", f"{len(warm_temp_df):,}")
    with col2:
        st.metric("Good Visibility Accidents", f"{len(good_vis_df):,}")
    with col3:
        st.metric("Both Conditions", f"{len(warm_good_df):,}")
    with col4:
        pct = (len(warm_good_df) / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
        st.metric("Percentage of Total", f"{pct:.1f}%")
    
    st.markdown("---")
    st.subheader("Top Reasons for Accidents")
    
    reasons = {
        "1. Driver Overconfidence": {
            "description": "Drivers feel safe when the weather is nice, so they pay less attention and drive faster.",
            "solutions": [
                "- Enforce speed limits more strictly during busy hours",
                "- Run awareness campaigns about driving risks even in good weather",
                "- Use variable speed signs based on road conditions"
            ]
        },
        "2. Increased Traffic Volume": {
            "description": "Nice weather encourages more people to go out, which increases traffic and accidents.",
            "solutions": [
                "- Use smart traffic lights to manage traffic better",
                "- Encourage carpooling and public transportation",
                "- Expand roads during busy seasons (peak)"
            ]
        },
        "3. Rush Hour Peaks": {
            "description": "Warm afternoons coincide with evening rush hours (3–6 PM), creating dangerous congestion.",
            "solutions": [
                "- Spread out work hours and encouraging companies to make remote work possible to reduce congestion",
                "- Improve public transport during rush hours",
                "- Place traffic officers at dangerous intersections"
            ]
        },
        "4. Sun Glare (Reduced Visibility)": {
            "description": "Even with good visibility, sunlight can create glare that makes it hard for drivers to see clearly.",
            "solutions": [
                "- Use reflective road signs",
                "- Improve street lighting and road markings",
                "- Add anti-glare barriers near intersections"
            ]
        },
        "5. Distracted Driving": {
            "description": "Good weather makes drivers relax and use phones or eat while driving.",
            "solutions": [
                "- Enforce strict laws against distracted driving",
                "- Run media awareness campaigns",
                "- Implement in-car technology that limits phone use while driving"
            ]
        },
        "6. Risky Maneuvers & Lane Changes": {
            "description": "Drivers take unsafe actions because they think the road is safe.",
            "solutions": [
                "- Use lane-keeping assist technology in vehicles",
                "- Increase penalties for unsafe lane changes",
                "- Improve lane markings and visibility"
            ]

        }
    }
    
    for reason, details in reasons.items():
        with st.expander(f"**{reason}**"):
            st.write(f"**Problem:** {details['description']}")
            st.write("**Solutions to Reduce Accidents:**")
            for solution in details['solutions']:
                st.write(solution)
    
    st.markdown("---")
    st.subheader("Accident Distribution by Hour (Warm & good Conditions)")
    
    warm_good_hourly = warm_good_df['Hour'].value_counts().sort_index()
    fig_warm_good = go.Figure(data=[
        go.Scatter(x=warm_good_hourly.index, y=warm_good_hourly.values, 
                   mode='lines+markers', fill='tozeroy', 
                   line=dict(color='#FF6B6B'), name='Accidents')
    ])
    fig_warm_good.update_layout(
        title="Hourly Distribution: Warm Temp & good Visibility Accidents",
        xaxis_title="Hour of Day",
        yaxis_title="Number of Accidents",
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_warm_good, use_container_width=True)
    
    st.markdown("---")
    st.subheader("Recommended Actions")
    st.warning("""
    **Priority Actions:**
    1. **Peak Hour Enforcement** - Deploy extra traffic enforcement 3–6 PM
    2. **Driver Education** - Campaign: "Good Weather ≠ Safe Driving"
    3. **Technology Deployment** - Install smart traffic management systems
    4. **Infrastructure Upgrade** - Improve road conditions during high-traffic seasons
    5. **Data Monitoring** - Track effectiveness of interventions monthly
    """)
