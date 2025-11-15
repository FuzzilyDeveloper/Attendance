
import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    df = pd.read_csv('attendance_dataset.csv', parse_dates=['Date', 'Check_In', 'Check_Out'])
    df['Hours_Worked'] = pd.to_numeric(df['Hours_Worked'], errors='coerce').fillna(0)
    df['OT_Hours'] = pd.to_numeric(df['OT_Hours'], errors='coerce').fillna(0)
    return df

df = load_data()
st.title("Data Visualization")

employees = st.multiselect("Select Employees", df['Employee_ID'].unique(), default=df['Employee_ID'].unique()[:5])
filtered = df[df['Employee_ID'].isin(employees)]

col1, col2, col3 = st.columns(3)
col1.metric("Total Employees", df['Employee_ID'].nunique())
col2.metric("Avg Hours/Day", f"{filtered['Hours_Worked'].mean():.2f}")
col3.metric("Total OT Hours", f"{filtered['OT_Hours'].sum():.0f}")

fig1 = px.line(filtered, x='Date', y='Hours_Worked', color='Employee_ID', title="Hours Worked Over Time")
st.plotly_chart(fig1, use_container_width=True)

fig2 = px.histogram(filtered, x='OT_Hours', color='Shift', title="Overtime Distribution")
st.plotly_chart(fig2, use_container_width=True)

st.dataframe(filtered.tail(20))
