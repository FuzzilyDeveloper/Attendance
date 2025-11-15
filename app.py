# app.py  ← Paste this entire file

import streamlit as st
import os

# === Page config & sidebar title ===
st.set_page_config(
    page_title="Employee Attendance Dashboard",
    page_icon="Office Worker",
    layout="wide"
)

st.sidebar.title("Navigation")

# === List of your pages (must match the .py filenames in the pages/ folder) ===
pages = {
    "Data Visualization": "1_Data_Visualization.py",
    "Prediction": "2_Prediction.py"
}

# === Sidebar selector ===
selected_page = st.sidebar.radio("Go to", list(pages.keys()))

# === Run the selected page safely ===
try:
    page_file = f"pages/{pages[selected_page]}"
    if os.path.exists(page_file):
        with open(page_file, "r", encoding="utf-8") as f:
            code = f.read()
        exec(code)
    else:
        st.error(f"Page file not found: {page_file}")
        st.info("Make sure the file exists in the 'pages/' folder with the exact name.")
except Exception as e:
    st.error("An error occurred while loading the page:")
    st.exception(e)
