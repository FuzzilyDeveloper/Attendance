
import streamlit as st
import pandas as pd
import joblib
import os
from sklearn.ensemble import RandomForestRegressor

@st.cache_data
def load_data():
    df = pd.read_csv('/content/attendance_dataset.csv', parse_dates=['Date', 'Check_In', 'Check_Out'])
    df['Hours_Worked'] = pd.to_numeric(df['Hours_Worked'], errors='coerce').fillna(0)
    df['OT_Hours']    = pd.to_numeric(df['OT_Hours'],    errors='coerce').fillna(0)
    return df

df = load_data()
st.title("Predict Hours Worked & Overtime")

def create_features(data: pd.DataFrame) -> pd.DataFrame:
    temp = data.copy()
    temp['DayOfWeek']   = temp['Date'].dt.dayofweek
    temp['IsWeekend']   = temp['DayOfWeek'].isin([5, 6]).astype(int)
    temp['Month']       = temp['Date'].dt.month
    temp['DayOfMonth']  = temp['Date'].dt.day
    temp = pd.get_dummies(temp, columns=['Shift', 'Status'], dtype=int)
    cols_to_drop = ['Employee_ID', 'Date', 'Check_In', 'Check_Out', 'index', 
                    'Hours_Worked', 'OT_Hours']
    temp = temp.drop(columns=[c for c in cols_to_drop if c in temp.columns], errors='ignore')
    return temp

model_path = "rf_hours_model.joblib"

@st.cache_resource
def get_model():
    if os.path.exists(model_path):
        return joblib.load(model_path)
    X = create_features(df)
    y = df['Hours_Worked']
    model = RandomForestRegressor(n_estimators=200, random_state=42, n_jobs=-1)
    model.fit(X, y)
    joblib.dump(model, model_path)
    st.success("Model trained and saved!")
    return model

model = get_model()

st.header("Make a New Prediction")
with st.form("prediction_form"):
    col1, col2 = st.columns(2)
    with col1:
        employee_id = st.text_input("Employee ID", "Emp_001")
        selected_date = st.date_input("Date", value=pd.to_datetime("today"))
    with col2:
        shift = st.selectbox("Shift", options=sorted(df['Shift'].unique()))
        status = st.selectbox("Status", options=sorted(df['Status'].unique()))
    submitted = st.form_submit_button("Predict Hours")
    if submitted:
        input_df = pd.DataFrame({'Date': [pd.to_datetime(selected_date)], 'Shift': [shift], 'Status': [status]})
        X_new = create_features(input_df)
        X_new = X_new.reindex(columns=model.feature_names_in_, fill_value=0)
        pred = model.predict(X_new)[0]
        st.success(f"**{employee_id}** on **{selected_date.strftime('%Y-%m-%d')}**")
        st.metric("Predicted Hours Worked", f"{pred:.2f} hours")
        if pred > 9: st.warning("High chance of overtime!")
